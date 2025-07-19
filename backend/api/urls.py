from django.urls import path

from .views import ProjectRequestCreateView

urlpatterns = [
    path(
        'project-request/',
        ProjectRequestCreateView.as_view(),
        name='project-request-create'
    ),
]
