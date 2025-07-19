from logging import getLogger

from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (ProjectRequestErrorResponseSerializer,
                          ProjectRequestResponseSerializer,
                          ProjectRequestSerializer)

logger = getLogger('api')


class ProjectRequestCreateView(APIView):
    """API для создания заявки на проект."""

    @extend_schema(
        operation_id='project_request_create',
        summary='Создать заявку на проект',
        description='Создание новой заявки на проект от клиента',
        tags=['Project Request'],
        request=ProjectRequestSerializer,
        responses={
            201: OpenApiResponse(
                description='Заявка успешно создана',
                response=ProjectRequestResponseSerializer,
            ),
            400: OpenApiResponse(
                description='Ошибка валидации входных данных',
                response=ProjectRequestErrorResponseSerializer,
            )
        }
    )
    def post(self, request: Request) -> Response:
        """Создание заявки на проект."""
        serializer = ProjectRequestSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            logger.info(f"Новая заявка от {instance.name} — {instance.email}")
            return Response({
                "success": True,
                "message": "Заявка успешно отправлена",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "success": False,
            "message": "Ошибка валидации данных",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
