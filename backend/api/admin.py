from typing import Optional

from django.contrib import admin
from django.http import HttpRequest
from django.utils.safestring import mark_safe

from .models import (
    CaseStudy,
    HomePageContent,
    Partner,
    ProjectRequest,
    Service,
    ServicePostscriptum,
    Tag,
    Technology,
)


@admin.register(ProjectRequest)
class ProjectRequestAdmin(admin.ModelAdmin):
    """Только просмотр заявок в админке"""

    readonly_fields = [
        "name",
        "company",
        "project_details",
        "phone_number",
        "email",
        "created_at",
    ]
    list_display = [
        "id",
        "name",
        "company",
        "phone_number",
        "email",
        "created_at",
    ]
    search_fields = ["name", "company", "phone_number", "email"]
    list_filter = ["company", "created_at"]
    ordering = ["-created_at"]

    def has_add_permission(self, request: HttpRequest) -> bool:
        """Запрет добавления заявок"""
        return False

    def has_change_permission(
        self, request: HttpRequest, obj: Optional[ProjectRequest] = None
    ) -> bool:
        """Запрет изменения заявок"""
        return False

    def has_delete_permission(
        self, request: HttpRequest, obj: Optional[ProjectRequest] = None
    ) -> bool:
        """Запрет удаления заявок"""
        return False


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    """Админка для модели парнёр."""

    list_display = ("name", "website", "get_logo")

    @admin.display(description="Лого")
    def get_logo(self, obj):
        """Возвращает лого."""
        return mark_safe(f"<img src={obj.image.url} width='80' height='60'>")


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    """Модель описывает управление технологиями блока Лаборатория стартапов."""

    list_display_links = ("name", "number")
    list_display = ("name", "number", "primary_info", "secondary_info")
    search_fields = ("name",)
    list_filter = ("number", "name")


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    """Админка для управления услугами"""

    list_display = ["id", "number", "name", "info", "tags_display"]
    list_display_links = ["id", "number", "name"]
    search_fields = ["name", "info", "content", "tags__name"]
    list_filter = ["number", "tags"]
    ordering = ["number"]

    fieldsets = (
        ("Основная информация", {"fields": ("number", "name", "info")}),
        ("Содержание услуги", {"fields": ("content",), "classes": ("wide",)}),
        ("Теги", {"fields": ("tags",), "classes": ("collapse",)}),
    )

    def tags_display(self, obj):
        """Отображение тегов в списке"""
        return ", ".join([tag.name for tag in obj.tags.all()])

    tags_display.short_description = "Теги"


@admin.register(ServicePostscriptum)
class ServicePostscriptumAdmin(admin.ModelAdmin):
    """Админка для управления постскриптумами услуг"""

    list_display = [
        "id",
        "name",
        "info",
        "item1",
        "item2",
        "item3",
        "item4",
    ]
    list_display_links = ["id", "name"]
    search_fields = ["name", "info"]
    list_filter = ["name"]
    ordering = ["name"]

    fieldsets = (
        ("Основная информация", {"fields": ("name", "info")}),
        (
            "Элементы постскриптума",
            {
                "fields": ("item1", "item2", "item3", "item4"),
                "classes": ("collapse",),
            },
        ),
    )

    def has_add_permission(self, request: HttpRequest) -> bool:
        """Запрет добавления новых записей, если уже есть одна"""
        if ServicePostscriptum.objects.exists():
            return False
        return True

    def has_delete_permission(
        self, request: HttpRequest, obj: Optional[ServicePostscriptum] = None
    ) -> bool:
        """Запрет удаления записей"""
        return False

    def get_actions(self, request):
        """Удаляем действие удаления из списка действий"""
        actions = super().get_actions(request)
        if "delete_selected" in actions:
            del actions["delete_selected"]
        return actions


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Админка для управления тегами"""

    list_display = ["id", "name"]
    list_display_links = ["id", "name"]
    search_fields = ["name"]
    ordering = ["name"]

    fieldsets = (("Основная информация", {"fields": ("name",)}),)


@admin.register(CaseStudy)
class CaseStudyAdmin(admin.ModelAdmin):
    """Админка для управления реальными проектами"""

    list_display = ["id", "service", "name", "info", "tags_display"]
    list_display_links = ["id", "name"]
    search_fields = ["name", "info", "service__name", "tags__name"]
    list_filter = ["service", "tags"]
    ordering = ["service", "name"]

    fieldsets = (
        ("Основная информация", {"fields": ("service", "name", "info")}),
        ("Теги", {"fields": ("tags",), "classes": ("collapse",)}),
    )

    def tags_display(self, obj):
        """Отображение тегов в списке"""
        return ", ".join([tag.name for tag in obj.tags.all()])

    tags_display.short_description = "Теги"


@admin.register(HomePageContent)
class HomePageAdmin(admin.ModelAdmin):
    """
    Админка для редактирования контента главной страницы.
    Допускается добавлять только один объект данной модели.
    """

    list_display_links = ("hero_title",)
    list_display = ("hero_title", "hero_subtitle")

    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(
        self, request: HttpRequest, obj: Optional[ProjectRequest] = None
    ) -> bool:
        """Запрет удаления главной страницы"""
        return False
