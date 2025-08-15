from http import HTTPStatus

from drf_spectacular.utils import OpenApiResponse, extend_schema

from api.serializers import (
    LegalPageResponseSerialize,
    LegalPageListResponseSerializer,
    LegalPageErrorResponseSerializer,
)


legal_page_list_schema = extend_schema(
    operation_id="legal_page_list",
    summary="Получить список технологий",
    tags=["Technologies"],
    responses={
        HTTPStatus.OK: OpenApiResponse(
            description="Данные успешно получены",
            response=LegalPageListResponseSerializer,
        ),
        HTTPStatus.BAD_REQUEST: OpenApiResponse(
            description="Неверные параметры запроса",
            response=LegalPageErrorResponseSerializer,
        ),
    },
)


legal_page_retrieve_schema = extend_schema(
    operation_id="legal_page_retrieve",
    summary="Получить технологию по slug",
    tags=["LegalPage"],
    responses={
        HTTPStatus.OK: OpenApiResponse(
            description="Данные успешно получены",
            response=LegalPageResponseSerialize,
        ),
        HTTPStatus.NOT_FOUND: OpenApiResponse(
            description="Страница не найдена",
            response=LegalPageErrorResponseSerializer,
        ),
        HTTPStatus.BAD_REQUEST: OpenApiResponse(
            description="Неверные параметры запроса",
            response=LegalPageErrorResponseSerializer,
        ),
    },
)
