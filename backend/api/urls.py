from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ProjectRequestCreateView, TechnologyViewSet, ServiceViewSet

router_v1 = DefaultRouter()
router_v1.register(r"technologies", TechnologyViewSet, basename="technologies")
router_v1.register(r"services", ServiceViewSet, basename="services")

urlpatterns = [
    path(
        "project-request/",
        ProjectRequestCreateView.as_view(),
        name="project-request-create",
    ),
    path("", include(router_v1.urls)),
]
