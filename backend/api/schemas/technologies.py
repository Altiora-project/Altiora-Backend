from http import HTTPStatus

from drf_spectacular.utils import OpenApiResponse, extend_schema

from api.serializers import (
    TechnologyErrorResponseSerializer,
    TechnologyListResponseSerializer,
    TechnologyResponseSerializer,
)


technologies_list_schema = extend_schema(
    operation_id="technologies_list",
    summary="Получить список технологий",
    tags=["Technologies"],
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
)


technology_retrieve_schema = extend_schema(
    operation_id="technology_retrieve",
    summary="Получить технологию по id",
    tags=["Technologies"],
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
)
