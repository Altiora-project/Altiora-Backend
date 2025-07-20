from django.db import models


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
