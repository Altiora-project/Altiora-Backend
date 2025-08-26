from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from api.sitemap import StaticSitemap
from api.views import RobotsTxtView
from .constants import API_VERSION

sitemaps = {
    "static": StaticSitemap,
}

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
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
