from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .managers import CustomUserManager

from django.dispatch import receiver

from defender import signals


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    shop_num = models.SmallIntegerField(default=0, verbose_name='Номер магазина')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['shop_num']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    #        email -> ldap
    def get_username(self):
        return self.email.split('@')[0].lower()

    # def get_user_id(self):
    #     return self.pk


# АУДИТ:
#  python manage.py cleanup_django_defender

@receiver(signals.username_block)
def username_blocked(username, **kwargs):
    print("%s was blocked!" % username)


@receiver(signals.ip_block)
def ip_blocked(ip_address, **kwargs):
    print("%s was blocked!" % ip_address)


@receiver(signals.username_unblock)
def username_unblock(username, **kwargs):
    print("%s was unblock!" % username)


@receiver(signals.ip_unblock)
def ip_blocked(ip_address, **kwargs):
    print("%s was unblock!" % ip_address)
