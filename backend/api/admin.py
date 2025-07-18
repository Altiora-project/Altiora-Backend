from django.contrib import admin

from .models import Technology


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
