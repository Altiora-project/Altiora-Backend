from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    HomePageContentView,
    PartnerViewSet,
    ProjectRequestCreateView,
    TechnologyViewSet,
    ServiceViewSet,
    SiteSettingsViewSet,
    PolicyViewSet,
)

router_v1 = DefaultRouter()
router_v1.register(r"technologies", TechnologyViewSet, basename="technologies")
router_v1.register(r"services", ServiceViewSet, basename="services")
router_v1.register(r"partners", PartnerViewSet, basename="partners")
router_v1.register(r"policies", PolicyViewSet, basename="policy")


urlpatterns = [
    path(
        "home-page-content/",
        HomePageContentView.as_view(),
        name="home-page-content",
    ),
    path(
        "project-request/",
        ProjectRequestCreateView.as_view(),
        name="project-request-create",
    ),
    path(
        "site-settings/",
        SiteSettingsViewSet.as_view(),
        name="site-settings",
    ),
    path("", include(router_v1.urls)),
]
