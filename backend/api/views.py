from http import HTTPStatus
from logging import getLogger

from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Technology
from .serializers import (
    ProjectRequestErrorResponseSerializer,
    ProjectRequestResponseSerializer,
    ProjectRequestSerializer,
    TechnologySerializer,
)

logger = getLogger("api")


class ProjectRequestCreateView(APIView):
    """API для создания заявки на проект."""

    @extend_schema(
        operation_id="project_request_create",
        summary="Создать заявку на проект",
        description="Создание новой заявки на проект от клиента",
        tags=["Project Request"],
        request=ProjectRequestSerializer,
        responses={
            HTTPStatus.CREATED: OpenApiResponse(
                description="Заявка успешно создана",
                response=ProjectRequestResponseSerializer,
            ),
            HTTPStatus.BAD_REQUEST: OpenApiResponse(
                description="Ошибка валидации входных данных",
                response=ProjectRequestErrorResponseSerializer,
            ),
        },
    )
    def post(self, request: Request) -> Response:
        """Создание заявки на проект."""
        serializer = ProjectRequestSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            logger.info(f"Новая заявка от {instance.name} — {instance.email}")
            return Response(
                {
                    "success": True,
                    "message": "Заявка успешно отправлена",
                    "data": serializer.data,
                },
                status=HTTPStatus.CREATED,
            )

        return Response(
            {
                "success": False,
                "message": "Ошибка валидации данных",
                "errors": serializer.errors,
            },
            status=HTTPStatus.BAD_REQUEST,
        )


class TechnologyViewSet(ReadOnlyModelViewSet):
    """Вьюсет для отображения технологий на странице Лаборатория стартапов."""

    queryset = Technology.objects.all()
    serializer_class = TechnologySerializer
