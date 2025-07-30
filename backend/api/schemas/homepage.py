from http import HTTPStatus

from drf_spectacular.utils import OpenApiResponse, extend_schema

from api.serializers import (
    HomePageContentErrorResponseSerializer,
    HomePageContentResponseSerializer,
)


home_page_content_schema = extend_schema(
    operation_id="home_page_content",
    summary="Получить контент главной страницы",
    description="Получение контента главной страницы",
    tags=["Home Page Content"],
    responses={
        HTTPStatus.OK: OpenApiResponse(
            description="Контент успешно получен",
            response=HomePageContentResponseSerializer,
        ),
        HTTPStatus.BAD_REQUEST: OpenApiResponse(
            description="Ошибка валидации входных данных",
            response=HomePageContentErrorResponseSerializer,
        ),
    },
)
