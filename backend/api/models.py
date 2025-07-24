from django.db import models
from django.core.exceptions import ValidationError
from ckeditor.fields import RichTextField

from altiora_backend import constants


class Partner(models.Model):
    """Модель партнёра."""

    name = models.CharField(
        verbose_name="Название партнёра",
        max_length=100,
        unique=True,
    )
    logo = models.ImageField(
        verbose_name="Логотип", upload_to="partners", blank=True, null=True
    )
    website = models.URLField(verbose_name="Сайт партнёра", blank=True)

    class Meta:
        ordering = ("name",)
        verbose_name = "Партнёр"
        verbose_name_plural = "Партнёры"

    def __str__(self):
        return self.name[:20]


class ProjectRequest(models.Model):
    """Модель для заявки на проект"""

    name = models.CharField(max_length=255, verbose_name="Имя")
    company = models.CharField(
        max_length=255, verbose_name="Название компании"
    )
    project_details = models.TextField(verbose_name="Детали проекта")
    phone_number = models.CharField(
        max_length=20, verbose_name="Номер телефона"
    )
    email = models.EmailField(max_length=255, verbose_name="Email")
    agreed_to_terms = models.BooleanField(
        verbose_name="Согласие с условиями", default=False
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания"
    )

    class Meta:
        verbose_name = "Заявка на проект"
        verbose_name_plural = "Заявки на проект"

    def __str__(self):
        return f"{self.name} — {self.company}"


class Technology(models.Model):
    """Модель для отображения технологий на странице Лаборатория стартапов."""

    name = models.CharField(
        max_length=constants.NAME_MAX_LENGTH,
        verbose_name="Название технологии",
    )
    number = models.PositiveSmallIntegerField(
        unique=True, verbose_name="Порядковый номер технологии"
    )
    image = models.ImageField(
        upload_to="technologies/",
        blank=True,
        null=True,
        verbose_name="Изображение",
    )
    primary_info = models.TextField(
        max_length=constants.INFO_MAX_LENGTH,
        verbose_name="Основная информация",
    )
    secondary_info = models.TextField(
        max_length=constants.INFO_MAX_LENGTH,
        blank=True,
        null=True,
        verbose_name="Дополнительная информация",
    )

    class Meta:
        default_related_name = "technology"
        verbose_name = "Технология"
        verbose_name_plural = "Технологии"
        ordering = ["number"]

    def __str__(self):
        return self.name


class ServicePostscriptum(models.Model):
    """Модель для постскриптума услуги."""

    name = models.CharField(
        max_length=constants.NAME_MAX_LENGTH, verbose_name="Название"
    )
    info = models.TextField(
        max_length=constants.TEXT_MAX_LENGTH, verbose_name="Информация"
    )
    item1 = models.CharField(
        max_length=constants.NAME_MAX_LENGTH, verbose_name="Элемент 1"
    )
    item2 = models.CharField(
        max_length=constants.NAME_MAX_LENGTH, verbose_name="Элемент 2"
    )
    item3 = models.CharField(
        max_length=constants.NAME_MAX_LENGTH, verbose_name="Элемент 3"
    )
    item4 = models.CharField(
        max_length=constants.NAME_MAX_LENGTH, verbose_name="Элемент 4"
    )

    class Meta:
        verbose_name = "Постскриптум услуги"
        verbose_name_plural = "Постскриптумы услуг"

    def clean(self):
        """Проверка, что существует только одна запись"""
        # Если это новая запись
        if not self.pk:
            exists = ServicePostscriptum.objects.exists()
            if exists:
                raise ValidationError(
                    "Может существовать только одна запись постскриптума"
                    + " услуги."
                )

    def save(self, *args, **kwargs):
        """Переопределение save для валидации"""
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Модель для тегов."""

    name = models.CharField(
        max_length=constants.NAME_MAX_LENGTH, verbose_name="Название тега"
    )

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Service(models.Model):
    """Модель для услуг."""

    name = models.CharField(
        max_length=constants.NAME_MAX_LENGTH, verbose_name="Название услуги"
    )
    number = models.PositiveSmallIntegerField(
        verbose_name="№ п/п в списке услуг"
    )
    info = models.TextField(
        max_length=constants.TEXT_MAX_LENGTH,
        verbose_name="Информация об услуге",
    )
    content = RichTextField(
        verbose_name="Содержание услуги", blank=True, null=True
    )
    tags = models.ManyToManyField(
        Tag, blank=True, related_name="services", verbose_name="Теги"
    )

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"
        ordering = ["number"]

    def __str__(self):
        return f"{self.number}. {self.name}"


class CaseStudy(models.Model):
    """Модель для реальных проектов."""

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="case_studies",
        verbose_name="Услуга",
    )
    name = models.CharField(
        max_length=constants.NAME_MAX_LENGTH, verbose_name="Название проекта"
    )
    info = models.TextField(
        max_length=constants.TEXT_MAX_LENGTH,
        verbose_name="Информация о проекте",
    )
    tags = models.ManyToManyField(
        Tag, blank=True, related_name="case_studies", verbose_name="Теги"
    )

    class Meta:
        verbose_name = "Реальный проект"
        verbose_name_plural = "Реальные проекты"
        ordering = ["service", "name"]

    def __str__(self):
        return f"{self.service.name} - {self.name}"
