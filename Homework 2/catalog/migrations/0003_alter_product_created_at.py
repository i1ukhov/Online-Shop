# Generated by Django 3.2.25 on 2024-05-30 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_auto_20240515_2222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='created_at',
            field=models.DateField(auto_now_add=True, verbose_name='Дата создания'),
        ),
    ]
