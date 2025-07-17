from django.db import models

from altiora_backend import constants


class Technology(models.Model):
    name = models.CharField(
        max_length=constants.NAME_MAX_LENGTH,
        verbose_name='Название технологии'
    )
    number = models.PositiveSmallIntegerField(
        verbose_name='Порядковый номер технологии'
    )
    image = models.ImageField(
        upload_to='technologies',
        blank=True,
        null=True,
        verbose_name='Изображение'
    )
    info_1 = models.TextField(
        max_length=constants.INFO_MAX_LENGTH,
        verbose_name='Основная информация'
    )
    info_2 = models.TextField(
        max_length=constants.INFO_MAX_LENGTH,
        blank=True,
        null=True,
        verbose_name='Дополнительная информация')

    class Meta:
        default_related_name = 'technology',
        verbose_name = 'Технология'
        verbose_name_plural = 'Технологии'
        ordering = ['number']

    def __str__(self):
        return self.name
