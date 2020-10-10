import json
import logging

from django.contrib.auth.backends import ModelBackend  # ,BaseBackend
from ldap3 import Server, Connection, SUBTREE, SYNC
# from django.contrib.auth.models import User

# import settings
# from accounts.models import Profile
from accounts.models import CustomUser

# logger = logging.getLogger(__name__)
# UserModel = get_user_model()

"""
Django authentication backend.
Указывает запрос LDAP, который выбирает пользователей для аутентификации. 
По умолчанию инициализация выполняется следующим образом (для Active Directory):
(&(objectClass=person)(userPrincipalName={uid}))
Для других серверов:
(&(objectClass=person)(cn={uid}))
print('User first name                 |', r[1]["givenName"][0].decode())
                print('User last name                  |', r[1]["sn"][0].decode())
"""


class Auth:
    __SERVER = 'ad.lmru.tech:389'  # getsecret('SERVER')  #
    # __AD_TREE = 'OU=Leroy Merlin Vostok,DC=hq,DC=ru,DC=corp,DC=leroymerlin,DC=com' # getsecret('AD_TREE')
    # getsecret('AD_TREE')
    __basedn = 'DC=hq,DC=ru,DC=corp,DC=leroymerlin,DC=com'

    __attr = ['physicalDeliveryOfficeName', 'postOfficeBox', 'mail', 'displayName']

    __query = '(&(objectCategory=Person)(sAMAccountName={})(!(sAMAccountName=*a)) \' +' \
              '(!(sAMAccountName=*s))(!(userAccountControl:1.2.840.113556.1.4.803:=2)))'

    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.shop_verbose = self.__connect()['physicalDeliveryOfficeName']
        self.shop_number = self.__connect()['postOfficeBox']
        self.mail = self.__connect()['mail']
        self.displayName = self.__connect()['displayName']

    def __connect(self, attr=None):
        if attr is None:
            attr = {}
        conn = Connection(Server(self.__SERVER), user=self.login + '@leroymerlin.ru', password=self.password,
                          client_strategy=SYNC)
        if conn.bind():
            # search_filter = '(&(objectCategory=Person)(sAMAccountName={}))'.format(self.login)
            search_filter = '(&(objectCategory=Person)(sAMAccountName={})(!(sAMAccountName=*a))(!(sAMAccountName=*s))(!(userAccountControl:1.2.840.113556.1.4.803:=2)))'.format(
                self.login)  # ('(&(objectCategory=Person)(sAMAccountName={}))').format(self.login)
            ''' 
                 User object filter     | (&(objectCategory=Person)(sAMAccountName=60*)(!(sAMAccountName=*a))(!(sAMAccountName=*s))(!(userAccountControl:1.2.840.113556.1.4.803:=2)))
                                                            | Starting with '60'. |                     |                     |
                                                                                  | No ending on 'a'.   |                     |
                                                                                                        | No ending on 's'.   |
                                                                                                                              | No disabled accounts, OID needed.
            '''
            # logger.info('Connection Bind Complete!')  # the last logged message from this method
            conn.search(self.__basedn, search_filter, SUBTREE,
                        attributes=self.__attr)
            # logger.info('SEARCHING COMPLETE')  # does not appear in the lo

            attr = json.loads(conn.response_to_json())
            try:
                attr = attr['entries'][0]['attributes']
                attr['postOfficeBox'] = attr['postOfficeBox'][0]
            except IndexError:  # Если Учётка не может получить данные, тогда не даём доступ.
                attr['physicalDeliveryOfficeName'] = None
                attr['postOfficeBox'] = None
                attr['mail'] = None
                attr['displayName'] = None
                return attr
            return attr

        else:  # Пользователь не найден.
            attr['physicalDeliveryOfficeName'] = None
            attr['postOfficeBox'] = None
            attr['mail'] = None
            attr['displayName'] = None
            # attr = None
            return attr
        # JsonResponse

    def ldap_correct(self):
        if self.shop_verbose and self.shop_number:
            return True
        else:
            return False


class AuthBackend(ModelBackend):
    # supports_object_permissions = True
    # supports_anonymous_user = False
    # supports_inactive_user = False

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None

    def authenticate(self, request, username=None, password=None, *args, **kwargs):
        print('inside custom auth:')
        if username.endswith('a'):
            print(f'До:{username}')
            username = username[:-1]
            print(f'После: {username}')

        user_auth = Auth(login=username, password=password)
        ''' Если пользователь есть в AD, то проверяем есть ли он в БД приложения и если нет, то создаём.'''
        if user_auth.ldap_correct():
            try:
                user = CustomUser.objects.get(email=user_auth.mail)
                # profile = Profile.objects.get(shop_num=user_auth.shop)
                # print(user_auth.displayName)
            except CustomUser.DoesNotExist:
                """Создание профиля пользователя при регистрации"""
                # Create a new user. There's no need to set a password
                # because only the password from settings.py is checked.
                user = CustomUser(email=user_auth.mail)
                user.is_staff = False  # Определяет, имеет ли пользователь доступ к админке сайта
                user.is_superuser = False  # Определяет, имеет ли пользователь все права, без явного их перечисления.
                user.shop_num = user_auth.shop_number
                user.save()
                # user = User.objects.get(username=username)
                # profile = Profile.objects.create(user=user, shop_num=user_auth.shop)
                # profile.save()
            # print(f'Авторизован как {user_auth.login}, {user_auth.displayName}')
            return user
        # Нет его в AD:
        else:

            print(f'Не верный ldap или пароль:{user_auth.login}')
            print(f'{user_auth.password}')
            return None

