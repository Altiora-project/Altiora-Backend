from typing import Optional

from django.contrib import admin
from django.http import HttpRequest
from django.utils.safestring import mark_safe

from .models import Partner, ProjectRequest, Technology


@admin.register(ProjectRequest)
class ProjectRequestAdmin(admin.ModelAdmin):
    """Только просмотр заявок в админке"""

    readonly_fields = [
        'name',
        'company',
        'project_details',
        'phone_number',
        'email',
        'created_at',
    ]
    list_display = [
        'id',
        'name',
        'company',
        'phone_number',
        'email',
        'created_at',
    ]
    search_fields = ['name', 'company', 'phone_number', 'email']
    list_filter = ['company', 'created_at']
    ordering = ['-created_at']

    def has_add_permission(self, request: HttpRequest) -> bool:
        """Запрет добавления заявок"""
        return False

    def has_change_permission(
            self,
            request: HttpRequest,
            obj: Optional[ProjectRequest] = None
    ) -> bool:
        """Запрет изменения заявок"""
        return False

    def has_delete_permission(
            self,
            request: HttpRequest,
            obj: Optional[ProjectRequest] = None
    ) -> bool:
        """Запрет удаления заявок"""
        return False


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    """Админка для модели парнёр."""

    list_display = ("name", "website", "get_logo")

    @admin.display(description='Лого')
    def get_logo(self, obj):
        """Возвращает лого."""
        return mark_safe(f"<img src={obj.image.url} width='80' height='60'>")


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    """Модель описывает управление технологиями блока Лаборатория стартапов."""

    list_display_links = (
        'name',
        'number'
    )
    list_display = (
        'name',
        'number',
        'primary_info',
        'secondary_info'
    )
    search_fields = ('name', )
    list_filter = ('number', 'name')
