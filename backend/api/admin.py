from typing import Optional

from django.contrib import admin
from django.http import HttpRequest

from .models import ProjectRequest


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
