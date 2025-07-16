from django.db import models


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
