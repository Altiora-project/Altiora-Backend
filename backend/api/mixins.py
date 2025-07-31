from django.db import models


class SeoMixin(models.Model):
    """Миксин для моделей услуг."""

    meta_title = models.CharField(
        verbose_name="Заголовок", max_length=100, blank=True, null=True
    )
    meta_description = models.TextField(
        verbose_name="Описание",
    )

    class Meta:
        abstract = True
