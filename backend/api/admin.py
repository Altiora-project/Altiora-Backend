from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Partner


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    """Админка для модели парнёр."""

    list_display = ("name", "website", "get_logo")

    @admin.display(description='Лого')
    def get_logo(self, obj):
        """Возвращает лого."""
        return mark_safe(f"<img src={obj.image.url} width='80' height='60'>")
