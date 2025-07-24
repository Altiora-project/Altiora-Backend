from django.db import models
from django.core.exceptions import ValidationError

from altiora_backend import constants



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


class HomePageContent(models.Model):
    """
    Модель для хранения всего уникального контента главной страницы.
    Использует кастомную логику в методе save, чтобы гарантировать,
    что в базе данных будет существовать только одна запись этой модели.
    """

    # --- Обновляемая мета-информация для SEO ---
    meta_title = models.CharField(
        verbose_name="SEO Заголовок",
        max_length=255,
        blank=True,
        help_text="Заголовок страницы для поисковых систем."
    )
    meta_description = models.TextField(
        verbose_name="SEO Описание",
        blank=True,
        help_text="Краткое описание страницы для поисковых систем."
    )

    # --- Блок Hero ---
    hero_title = models.CharField(
        verbose_name="Главный заголовок (Hero)",
        max_length=200
    )
    hero_subtitle = models.TextField(
        verbose_name="Подзаголовок (Hero)"
    )
    hero_image = models.ImageField(
        verbose_name="Изображение (Hero)",
        upload_to="main_page/",
        blank=True,
        null=True
    )

    # --- Блок "О нас" ---
    about_title = models.CharField(
        verbose_name="Заголовок 'О нас'",
        max_length=200
    )
    about_text = models.TextField(
        verbose_name="Текст 'О нас'"
    )
    higlight_1 = models.CharField(
        verbose_name="Хайлайт блока 'О нас' "
        max_length=200
    )
    higlight_2 = models.CharField(
        verbose_name="Хайлайт блока 'О нас'"
        max_length=200
    )


    # --- Блок "Наши услуги" ---
    services_section_title = models.CharField(
        verbose_name="Заголовок секции 'Наши услуги'",
        max_length=200,
        default="/наши услуги"
    )

    # --- Блок "Лаборатория стартапов" (описание для главной страницы) ---
    lab_title = models.CharField(
        verbose_name="Заголовок 'Лаборатория стартапов'",
        max_length=200,
        default='/лаборатория стартапов'
    )
    lab_description = models.TextField(
        verbose_name="Краткое описание 'Лаборатории'"
    )

    # --- Блок "digital маркетинг" (описание для главной страницы) ---
    lab_title = models.CharField(
        verbose_name="Заголовок 'digital маркетинг'",
        max_length=200,
        default='/digital маркетинг'
    )
    lab_description = models.TextField(
        verbose_name="Краткое описание 'digital маркетинг'"
    )

    # --- Блок "Токенизация активов и ЦФА" ---
    tokenization_title = models.CharField(
        verbose_name="Заголовок 'Токенизация'",
        max_length=200
        default='/токенизация активов и цфа'
    )
    tokenization_description = models.TextField(
        verbose_name="Описание 'Токенизация'"
    )
    tokenization_video_url = models.URLField(
        verbose_name="URL видео 'Токенизация'",
        blank=True,
        help_text="Ссылка на видео, например, с YouTube или Vimeo."
    )

    # --- Блок "Партнеры" ---
    partners_section_title = models.CharField(
        verbose_name="Заголовок секции 'Партнеры'",
        max_length=200,
        default="/партнеры"
    )

    # --- Блок "Заказать проект" ---
    partners_section_title = models.CharField(
        verbose_name="Заголовок секции 'Заказать проект'",
        max_length=200,
        default="/заказать проект"
    )

    # --- Блок "Контакты" ---
    contacts_title = models.CharField(
        verbose_name="Заголовок 'Контакты'",
        max_length=200,
        default="/контакты"
    )
    contact_address = models.CharField(
        verbose_name="Адрес",
        max_length=255,
        blank=True
    )
    contact_phone = models.CharField(
        verbose_name="Телефон",
        max_length=50,
        blank=True
    )
    contact_email = models.EmailField(
        verbose_name="Email",
        blank=True
    )

    class Meta:
        verbose_name = "Контент главной страницы"
        verbose_name_plural = "Контент главной страницы"

    def __str__(self):
        return f"Контент главной страницы"

    def save(self, *args, **kwargs):
        """
        Переопределенный метод сохранения.
        Запрещает создание нового объекта, если один уже существует.
        """
        if not self.pk and HomePageContent.objects.exists():
            raise ValidationError(
                'Может существовать только один экземпляр контента для главной страницы.'
                'Пожалуйста, редактируйте уже существующий.'
            )
        return super().save(*args, **kwargs)