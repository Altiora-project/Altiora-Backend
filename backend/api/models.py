from django.db import models

from altiora_backend import constants


class Partner(models.Model):
    """Модель партнёра."""

    name = models.CharField(
        verbose_name="Название партнёра",
        max_length=100,
        unique=True,
    )
    logo = models.ImageField(
        verbose_name="Логотип",
        upload_to="partners",
        blank=True,
        null=True
    )
    website = models.URLField(
        verbose_name="Сайт партнёра",
        blank=True
    )

    class Meta:
        ordering = ("name",)
        verbose_name = "Партнёр"
        verbose_name_plural = "Партнёры"

    def __str__(self):
        return self.name[:20]


class ProjectRequest(models.Model):
    """Модель для заявки на проект"""

    name = models.CharField(
        max_length=255,
        verbose_name="Имя"
    )
    company = models.CharField(
        max_length=255,
        verbose_name="Название компании"
    )
    project_details = models.TextField(
        verbose_name="Детали проекта"
    )
    phone_number = models.CharField(
        max_length=20,
        verbose_name="Номер телефона"
    )
    email = models.EmailField(
        max_length=255,
        verbose_name="Email"
    )
    agreed_to_terms = models.BooleanField(
        verbose_name="Согласие с условиями",
        default=False
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )

    class Meta:
        verbose_name = "Заявка на проект"
        verbose_name_plural = "Заявки на проект"

    def __str__(self):
        return f"{self.name} — {self.company}"


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
    primary_info = models.TextField(
        max_length=constants.INFO_MAX_LENGTH,
        verbose_name='Основная информация'
    )
    secondary_info = models.TextField(
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
