from http import HTTPStatus
from logging import getLogger

from altiora_backend.constants import ROBOTS_TXT_TEMPLATE
from django.http import HttpRequest, HttpResponse
from drf_spectacular.utils import (
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from django.http import Http404

from .models import Technology, Service
from .serializers import (
    ProjectRequestErrorResponseSerializer,
    ProjectRequestResponseSerializer,
    ProjectRequestSerializer,
    TechnologyErrorResponseSerializer,
    TechnologyListResponseSerializer,
    TechnologyResponseSerializer,
    TechnologySerializer,
    ServiceDetailSerializer,
    ServiceDetailDocResponseSerializer,
    ServiceListSimpleSerializer,
    ServiceListResponseSerializer,
    ServiceDetailResponseSerializer,
    ServiceErrorResponseSerializer,
    CaseStudySerializer,
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


@extend_schema(
    tags=["Technologies"],
)
@extend_schema_view(
    list=extend_schema(
        operation_id="technologies_list",
        summary="Получить список технологий",
        responses={
            HTTPStatus.OK: OpenApiResponse(
                description="Данные успешно получены",
                response=TechnologyListResponseSerializer,
            ),
            HTTPStatus.BAD_REQUEST: OpenApiResponse(
                description="Неверные параметры запроса",
                response=TechnologyErrorResponseSerializer,
            ),
        },
    ),
    retrieve=extend_schema(
        operation_id="technology_retrieve",
        summary="Получить технологию по id",
        responses={
            HTTPStatus.OK: OpenApiResponse(
                description="Данные успешно получены",
                response=TechnologyResponseSerializer,
            ),
            HTTPStatus.NOT_FOUND: OpenApiResponse(
                description="Технология не найдена",
                response=TechnologyErrorResponseSerializer,
            ),
            HTTPStatus.BAD_REQUEST: OpenApiResponse(
                description="Неверные параметры запроса",
                response=TechnologyErrorResponseSerializer,
            ),
        },
    ),
)
class TechnologyViewSet(ReadOnlyModelViewSet):
    """Вьюсет для отображения технологий на странице Лаборатория стартапов."""

    queryset = Technology.objects.all()
    serializer_class = TechnologySerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        response_serializer = TechnologyListResponseSerializer(
            {
                "success": True,
                "message": "Список технологий получен",
                "data": serializer.data,
            }
        )
        return Response(response_serializer.data, status=HTTPStatus.OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        response_serializer = TechnologyResponseSerializer(
            {
                "success": True,
                "message": "Технология получена",
                "data": serializer.data,
            }
        )
        return Response(response_serializer.data, status=HTTPStatus.OK)


class RobotsTxtView(APIView):
    """Вью для robots.txt."""

    @extend_schema(
        operation_id="robots_txt",
        summary="Получить robots.txt",
        description=(
            "Возвращает содержимое файла robots.txt для поисковых роботов"
        ),
        tags=["SEO"],
        responses={
            HTTPStatus.OK: OpenApiResponse(
                description="robots.txt успешно получен",
            ),
        },
    )
    def get(self, request: HttpRequest) -> HttpResponse:
        """Формирует robots.txt с актуальной схемой и хостом."""
        content = ROBOTS_TXT_TEMPLATE.format(
            scheme=request.scheme, host=request.get_host()
        )
        return HttpResponse(content, content_type="text/plain")


@extend_schema(
    tags=["Services"],
)
@extend_schema_view(
    list=extend_schema(
        operation_id="services_list",
        summary="Получить список услуг и проектов",
        responses={
            HTTPStatus.OK: OpenApiResponse(
                description="Данные успешно получены",
                response=ServiceListResponseSerializer,
            ),
            HTTPStatus.BAD_REQUEST: OpenApiResponse(
                description="Неверные параметры запроса",
                response=ServiceErrorResponseSerializer,
            ),
        },
    ),
    retrieve=extend_schema(
        operation_id="service_retrieve",
        summary="Получить услугу по id",
        responses={
            HTTPStatus.OK: OpenApiResponse(
                description="Данные успешно получены",
                response=ServiceDetailDocResponseSerializer,
            ),
            HTTPStatus.NOT_FOUND: OpenApiResponse(
                description="Услуга не найдена",
                response=ServiceErrorResponseSerializer,
            ),
            HTTPStatus.BAD_REQUEST: OpenApiResponse(
                description="Неверные параметры запроса",
                response=ServiceErrorResponseSerializer,
            ),
        },
    ),
)
class ServiceViewSet(ReadOnlyModelViewSet):
    """Вьюсет для отображения услуг на странице услуг."""

    queryset = Service.objects.all()
    serializer_class = ServiceListSimpleSerializer

    def get_serializer_class(self):
        """Возвращает сериализатор в зависимости от действия."""
        if self.action == "retrieve":
            return ServiceDetailSerializer
        return ServiceListSimpleSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        services_serializer = self.get_serializer(queryset, many=True)

        # Получаем все записи CaseStudy
        from .models import CaseStudy

        case_studies = CaseStudy.objects.all()
        case_studies_serializer = CaseStudySerializer(case_studies, many=True)

        response_serializer = ServiceListResponseSerializer(
            {
                "success": True,
                "message": "Список услуг и проектов получен",
                "data": {
                    "services": services_serializer.data,
                    "case_studies": case_studies_serializer.data,
                },
            }
        )
        return Response(response_serializer.data, status=HTTPStatus.OK)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            response_serializer = ServiceDetailResponseSerializer(
                {
                    "success": True,
                    "message": "Услуга получена",
                    "data": serializer.data,
                }
            )
            return Response(response_serializer.data, status=HTTPStatus.OK)
        except Http404:
            response_serializer = ServiceErrorResponseSerializer(
                {
                    "success": False,
                    "message": "Услуга не найдена",
                    "errors": {
                        "detail": ["Услуга с указанным ID не существует"]
                    },
                }
            )
            return Response(
                response_serializer.data, status=HTTPStatus.NOT_FOUND
            )
