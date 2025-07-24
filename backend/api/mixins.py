from django.db import models


class ServiceSeoMixin(models.Model):
    """Миксин для моделей услуг."""

    seo_title = models.CharField(
        verbose_name="Заголовок", max_length=100, unique=True
    )
    seo_description = models.TextField(
        verbose_name="Описание",
    )

    class Meta:
        abstract = True
