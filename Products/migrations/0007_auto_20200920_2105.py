# Generated by Django 3.1.1 on 2020-09-20 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0006_auto_20200920_2102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foundgoods',
            name='update_at',
            field=models.DateField(blank=True, db_index=True, help_text='Пожалуйста, используйте следующий формат: <em>ДД.ММ.ГГГГ</em>. Товар выдан, если дата установлена', null=True, verbose_name='выдан'),
        ),
    ]
