from http import HTTPStatus

from drf_spectacular.utils import OpenApiResponse, extend_schema

from api.serializers import (
    PolicyResponseSerializer,
    PolicyListResponseSerializer,
    PolicyErrorResponseSerializer,
)


policy_list_schema = extend_schema(
    operation_id="policy_list",
    summary="Получить список юридических страниц",
    tags=["Policy"],
    responses={
        HTTPStatus.OK: OpenApiResponse(
            description="Данные успешно получены",
            response=PolicyListResponseSerializer,
        ),
        HTTPStatus.BAD_REQUEST: OpenApiResponse(
            description="Неверные параметры запроса",
            response=PolicyErrorResponseSerializer,
        ),
    },
)


policy_retrieve_schema = extend_schema(
    operation_id="policy_retrieve",
    summary="Получить юридическую страницу по slug",
    tags=["Policy"],
    responses={
        HTTPStatus.OK: OpenApiResponse(
            description="Данные успешно получены",
            response=PolicyResponseSerializer,
        ),
        HTTPStatus.NOT_FOUND: OpenApiResponse(
            description="Страница не найдена",
            response=PolicyErrorResponseSerializer,
        ),
        HTTPStatus.BAD_REQUEST: OpenApiResponse(
            description="Неверные параметры запроса",
            response=PolicyErrorResponseSerializer,
        ),
    },
)
