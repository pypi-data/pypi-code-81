
import datetime

from django.db import models


class Product(models.Model):
    """Товар"""
    name = models.TextField(
        max_length=30,
        verbose_name='Наименование товара',
    )

    shelf_life = models.DurationField(
        verbose_name='Срок годности',
    )

    class Meta:
        app_label = 'tests'


class Storage(models.Model):
    """Хранилище товаров"""
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Товар',
    )

    date_of_delivery = models.DateTimeField(
        verbose_name='Дата и время привоза на склад',
        default=datetime.datetime.now,
    )

    date_of_manufacture = models.DateField(
        verbose_name='Дата создания товара',
    )

    class Meta:
        app_label = 'tests'


class Catalogue(models.Model):
    """Каталог магазина"""
    storage = models.OneToOneField(
        Storage,
        on_delete=models.CASCADE,
        verbose_name='Товар на складе',
    )

    date_of_add = models.DateField(
        verbose_name=(
            'Дата добавления продукта в каталог'),
        default=datetime.datetime.now,
    )

    class Meta:
        app_label = 'tests'
