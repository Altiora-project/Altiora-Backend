from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ProjectRequestCreateView, TechnologyViewSet

router_v1 = DefaultRouter()
router_v1.register(r"technologies", TechnologyViewSet, basename="technologies")

urlpatterns = [
    path(
        "project-request/",
        ProjectRequestCreateView.as_view(),
        name="project-request-create",
    ),
    path("", include(router_v1.urls)),
]
