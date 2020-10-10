from django.db import models
# from django.db.models.signals import post_save
# from django.dispatch import receiver
from django.urls import reverse_lazy
# from django.utils import timezone
# from django.utils.timezone import get_current_timezone

from accounts.models import CustomUser

'''Таблица забытого товара'''


class FoundGoods(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='Номер заявки')
    bar_code = models.CharField(max_length=50, unique=False, verbose_name='Штрихкод', blank=False, db_index=True
                                )
    lm_code = models.CharField(max_length=15, verbose_name='ЛМ-код', blank=False, db_index=True)
    caption = models.CharField(max_length=50, verbose_name='Наименование', blank=False)
    amount_goods = models.FloatField(verbose_name='Количество', null=True)  # КоличествоТОвара
    note_add = models.CharField(max_length=50, verbose_name='Заметка', blank=True, null=True)
    user = models.ForeignKey(CustomUser, verbose_name='Пользователь', on_delete=models.PROTECT,
                             related_name='custom_user', blank=True)

    shop_num = models.PositiveSmallIntegerField(verbose_name='Номер магазина', blank=True, null=True)

    create_at = models.DateField(verbose_name='найден',
                                 auto_now_add=True,
                                 db_index=True)  # Дата "Найден" auto_now_add=True - Автоматом создаётся только один раз

    update_at = models.DateField(verbose_name='выдан', auto_now=False, blank=True,
                                 null=True, help_text="Пожалуйста, используйте следующий формат: "
                                                      "<em>ДД.ММ.ГГГГ</em>. Товар выдан, если дата установлена",
                                 db_index=True)  # Null = True auto_now - Изменяется кажлый раз при измененение.

    def get_absolute_url(self):
        return reverse_lazy('UpdateProduct', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.pk} {self.bar_code}, {self.lm_code}, {self.caption}, {self.amount_goods}'

    class Meta:
        verbose_name = 'Забытый товар'
        verbose_name_plural = 'Забытые товары'
        # ordering = ['-create_at']


'''Таблица товара'''


class Catalog(models.Model):
    ean = models.CharField(max_length=20, verbose_name='Штрих Код', db_index=True)
    lm = models.CharField(max_length=10, verbose_name='ЛМ код', db_index=True)
    product_name = models.CharField(max_length=255, verbose_name='Наименование')

    def __str__(self):
        return f'{self.ean}, {self.lm}, {self.product_name}'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

#
# @receiver(post_save, sender=FoundGoods)
# def create_user_profile(sender, instance, created, **kwargs):
#     """Создание профиля пользователя при регистрации"""
#     if created:
#         FoundGoods.objects.create(user=instance, id=instance.id)
#         instance.profile.save()
