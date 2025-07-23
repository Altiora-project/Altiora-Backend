from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView

from .constants import API_VERSION

urlpatterns = [
    path("admin/", admin.site.urls),
    path(f"api/{API_VERSION}/", include("api.urls")),
    # Эндпоинт схемы OpenAPI
    path(
        f"api/{API_VERSION}/schema/",
        SpectacularAPIView.as_view(),
        name="schema",
    ),
    # Документация Redoc
    path(
        f"api/{API_VERSION}/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]
