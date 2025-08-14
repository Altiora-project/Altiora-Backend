from http import HTTPStatus

from drf_spectacular.utils import OpenApiResponse, extend_schema

from api.serializers import (
    SiteSettingsResponseSerializer,
    SiteSettingsErrorResponseSerializer,
)


site_settings_schema = extend_schema(
    operation_id="site_settings_static",
    summary="Получить контент статики",
    description="Получение контента статики",
    tags=["Site Settings"],
    responses={
        HTTPStatus.OK: OpenApiResponse(
            description="Контент успешно получен",
            response=SiteSettingsResponseSerializer,
        ),
        HTTPStatus.BAD_REQUEST: OpenApiResponse(
            description="Ошибка валидации входных данных",
            response=SiteSettingsErrorResponseSerializer,
        ),
    },
)
