from http import HTTPStatus

from drf_spectacular.utils import OpenApiResponse, extend_schema

from api.serializers import (
    ServiceDetailDocResponseSerializer,
    ServiceErrorResponseSerializer,
    ServiceListResponseSerializer,
)


services_list_schema = extend_schema(
    operation_id="services_list",
    summary="Получить список услуг и проектов",
    tags=["Services"],
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
)


service_retrieve_schema = extend_schema(
    operation_id="service_retrieve",
    summary="Получить услугу по slug",
    tags=["Services"],
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
)
