from api.views import RobotsTxtView
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from .constants import API_VERSION

urlpatterns = [
    path("robots.txt/", RobotsTxtView.as_view(), name="robots.txt"),
    path("admin/", admin.site.urls),
    path(f"api/{API_VERSION}/", include("api.urls")),
    path("mdeditor/", include("mdeditor.urls")),
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
    # Документация Swagger
    path(
        f"api/{API_VERSION}/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger",
    ),
]
