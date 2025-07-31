from django.db import models
from django.core.exceptions import ValidationError
from ckeditor.fields import RichTextField

from altiora_backend import constants

from .mixins import SeoMixin


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


class Service(SeoMixin):
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


class HomePageContent(SeoMixin):
    """
    Модель для хранения всего уникального контента главной страницы.
    Использует кастомную логику в методе save, чтобы гарантировать,
    что в базе данных будет существовать только одна запись этой модели.
    """

    # --- Обновляемая мета-информация для SEO ---
    meta_title = models.CharField(
        verbose_name="SEO Заголовок",
        max_length=constants.NAME_MAX_LENGTH,
        blank=True,
        help_text="Заголовок страницы для поисковых систем.",
    )
    meta_description = models.TextField(
        verbose_name="SEO Описание",
        blank=True,
        help_text="Краткое описание страницы для поисковых систем.",
    )

    # --- Блок Hero ---
    hero_title = models.CharField(
        verbose_name="Главный заголовок (Hero)",
        max_length=constants.NAME_MAX_LENGTH,
    )
    hero_subtitle = models.TextField(verbose_name="Подзаголовок (Hero)")
    hero_image = models.ImageField(
        verbose_name="Изображение (Hero)",
        upload_to="main_page/",
        blank=True,
        null=True,
    )

    # --- Блок "О нас" ---
    about_title = models.CharField(
        verbose_name="Заголовок 'О нас'", max_length=constants.NAME_MAX_LENGTH
    )
    about_text = RichTextField(verbose_name="Текст 'О нас'")
    higlight_1 = models.CharField(
        verbose_name="Хайлайт блока 'О нас' №1",
        max_length=constants.NAME_MAX_LENGTH,
    )
    higlight_2 = models.CharField(
        verbose_name="Хайлайт блока 'О нас' №2",
        max_length=constants.NAME_MAX_LENGTH,
    )

    # --- Блок "Наши услуги" ---
    services_section_title = models.CharField(
        verbose_name="Заголовок секции 'Наши услуги'",
        max_length=constants.NAME_MAX_LENGTH,
        default="/наши услуги",
    )

    # --- Блок "Лаборатория стартапов" (описание для главной страницы) ---
    lab_title = models.CharField(
        verbose_name="Заголовок 'Лаборатория стартапов'",
        max_length=constants.NAME_MAX_LENGTH,
        default="/лаборатория стартапов",
    )
    lab_description = RichTextField(
        verbose_name="Краткое описание 'Лаборатории'"
    )

    # --- Блок "digital маркетинг" (описание для главной страницы) ---
    dig_title = models.CharField(
        verbose_name="Заголовок 'digital маркетинг'",
        max_length=constants.NAME_MAX_LENGTH,
        default="/digital маркетинг",
    )
    dig_description = RichTextField(
        verbose_name="Краткое описание 'digital маркетинг'"
    )

    # --- Блок "Токенизация активов и ЦФА" ---
    tokenization_title = models.CharField(
        verbose_name="Заголовок 'Токенизация'",
        max_length=constants.NAME_MAX_LENGTH,
        default="/токенизация активов и цфа",
    )
    tokenization_description = RichTextField(
        verbose_name="Описание 'Токенизация'"
    )
    tokenization_video_url = models.URLField(
        verbose_name="URL видео 'Токенизация'",
        blank=True,
        help_text="Ссылка на видео, например, с YouTube или Vimeo.",
    )
    tokenization_links = RichTextField(
        verbose_name="Дополнительная информация"
    )

    # --- Блок "Партнеры" ---
    partners_section_title = models.CharField(
        verbose_name="Заголовок секции 'Партнеры'",
        max_length=constants.NAME_MAX_LENGTH,
        default="/партнеры",
    )

    # --- Блок "Заказать проект" ---
    order_section_title = models.CharField(
        verbose_name="Заголовок секции 'Заказать проект'",
        max_length=constants.NAME_MAX_LENGTH,
        default="/заказать проект",
    )

    # --- Блок "Контакты" ---
    contacts_title = models.CharField(
        verbose_name="Заголовок 'Контакты'",
        max_length=constants.NAME_MAX_LENGTH,
        default="/контакты",
    )
    contact_address = models.CharField(
        verbose_name="Адрес", max_length=constants.NAME_MAX_LENGTH, blank=True
    )
    contact_phone = models.CharField(
        verbose_name="Телефон",
        max_length=constants.NAME_MAX_LENGTH,
        blank=True,
    )
    contact_email = models.EmailField(verbose_name="Email", blank=True)

    class Meta:
        verbose_name = "Контент главной страницы"
        verbose_name_plural = "Контент главной страницы"

    def __str__(self):
        return "Контент главной страницы"

    def save(self, *args, **kwargs):
        """
        Переопределенный метод сохранения.
        Запрещает создание нового объекта, если один уже существует.
        """
        if not self.pk and HomePageContent.objects.exists():
            raise ValidationError(
                "Может существовать только один экземпляр главной страницы."
                "Пожалуйста, редактируйте уже существующий."
            )
        return super().save(*args, **kwargs)
