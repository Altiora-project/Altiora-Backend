from typing import Optional

from django.contrib import admin
from django.http import HttpRequest

from .models import ProjectRequest, Technology, ServicePostscriptum, Service, ServiceContent, Tag, CaseStudy


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


@admin.register(ServicePostscriptum)
class ServicePostscriptumAdmin(admin.ModelAdmin):
    """Админка для управления постскриптумами услуг"""

    list_display = [
        'id',
        'name',
        'info',
        'item1',
        'item2',
        'item3',
        'item4',
    ]
    list_display_links = ['id', 'name']
    search_fields = ['name', 'info']
    list_filter = ['name']
    ordering = ['name']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'info')
        }),
        ('Элементы постскриптума', {
            'fields': ('item1', 'item2', 'item3', 'item4'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    """Админка для управления услугами"""

    list_display = [
        'id',
        'number',
        'name',
        'info',
        'contents_count',
        'tags_display'
    ]
    list_display_links = ['id', 'number', 'name']
    search_fields = ['name', 'info', 'tags__name']
    list_filter = ['number', 'tags']
    ordering = ['number']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('number', 'name', 'info')
        }),
        ('Теги', {
            'fields': ('tags',),
            'classes': ('collapse',)
        }),
    )

    def contents_count(self, obj):
        """Количество составов услуги"""
        return obj.contents.count()
    contents_count.short_description = "Количество составов"

    def tags_display(self, obj):
        """Отображение тегов в списке"""
        return ", ".join([tag.name for tag in obj.tags.all()])
    tags_display.short_description = "Теги"


@admin.register(ServiceContent)
class ServiceContentAdmin(admin.ModelAdmin):
    """Админка для управления составами услуг"""

    list_display = [
        'id',
        'service',
        'number',
        'name',
        'info'
    ]
    list_display_links = ['id', 'number', 'name']
    search_fields = ['name', 'info', 'service__name']
    list_filter = ['service', 'number']
    ordering = ['service', 'number']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('service', 'number', 'name', 'info')
        }),
    )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Админка для управления тегами"""

    list_display = [
        'id',
        'name'
    ]
    list_display_links = ['id', 'name']
    search_fields = ['name']
    ordering = ['name']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name',)
        }),
    )


@admin.register(CaseStudy)
class CaseStudyAdmin(admin.ModelAdmin):
    """Админка для управления реальными проектами"""

    list_display = [
        'id',
        'service',
        'name',
        'info',
        'tags_display'
    ]
    list_display_links = ['id', 'name']
    search_fields = ['name', 'info', 'service__name', 'tags__name']
    list_filter = ['service', 'tags']
    ordering = ['service', 'name']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('service', 'name', 'info')
        }),
        ('Теги', {
            'fields': ('tags',),
            'classes': ('collapse',)
        }),
    )

    def tags_display(self, obj):
        """Отображение тегов в списке"""
        return ", ".join([tag.name for tag in obj.tags.all()])
    tags_display.short_description = "Теги"
