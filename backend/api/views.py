from http import HTTPStatus
from logging import getLogger

from altiora_backend.constants import ROBOTS_TXT_TEMPLATE
from django.http import HttpRequest, HttpResponse
from drf_spectacular.utils import extend_schema_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet
from rest_framework.mixins import ListModelMixin
from django.http import Http404

from .models import HomePageContent, Partner, Technology, Service
from .serializers import (
    HomePageContentSerializer,
    HomePageContentResponseSerializer,
    PartnerSerializer,
    ProjectRequestSerializer,
    TechnologySerializer,
    TechnologyListResponseSerializer,
    TechnologyResponseSerializer,
    ServiceDetailSerializer,
    ServiceDetailResponseSerializer,
    ServiceListSimpleSerializer,
    ServiceListResponseSerializer,
    ServiceErrorResponseSerializer,
    CaseStudySerializer,
)
from .schemas import (
    home_page_content_schema,
    project_request_create_schema,
    technologies_list_schema,
    technology_retrieve_schema,
    partners_list_schema,
    services_list_schema,
    service_retrieve_schema,
    robots_txt_schema,
)

logger = getLogger("api")


class HomePageContentView(APIView):
    """API для получения контента главной страницы."""

    @home_page_content_schema
    def get(self, request: Request) -> Response:
        """Получение контента главной страницы."""
        instance = HomePageContent.objects.first()
        if not instance:
            return Response(
                {
                    "success": False,
                    "message": "Контент главной страницы не найден",
                    "data": {},
                },
                status=HTTPStatus.NOT_FOUND,
            )
        inner_data = HomePageContentSerializer(instance).data

        response_data = {
            "success": True,
            "message": "Контент главной страницы",
            "data": inner_data,
        }
        serializer = HomePageContentResponseSerializer(data=response_data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=HTTPStatus.OK)


class ProjectRequestCreateView(APIView):
    """API для создания заявки на проект."""

    @project_request_create_schema
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


@extend_schema_view(
    list=technologies_list_schema,
    retrieve=technology_retrieve_schema,
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


@extend_schema_view(
    list=partners_list_schema,
)
class PartnerViewSet(ListModelMixin, GenericViewSet):
    """Вьюсет для отображения партнеров на странице Партнеры."""

    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer


class RobotsTxtView(APIView):
    """Вью для robots.txt."""

    @robots_txt_schema
    def get(self, request: HttpRequest) -> HttpResponse:
        """Формирует robots.txt с актуальной схемой и хостом."""
        content = ROBOTS_TXT_TEMPLATE.format(
            scheme=request.scheme, host=request.get_host()
        )
        return HttpResponse(content, content_type="text/plain")


@extend_schema_view(
    list=services_list_schema,
    retrieve=service_retrieve_schema,
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
