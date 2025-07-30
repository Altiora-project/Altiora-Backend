from http import HTTPStatus

from drf_spectacular.utils import OpenApiResponse, extend_schema

from api.serializers import (
    PartnerErrorResponseSerializer,
    PartnerResponseSerializer,
)


partners_list_schema = extend_schema(
    operation_id="partners_list",
    summary="Получить список партнеров",
    tags=["Partners"],
    responses={
        HTTPStatus.OK: OpenApiResponse(
            description="Данные успешно получены",
            response=PartnerResponseSerializer,
        ),
        HTTPStatus.BAD_REQUEST: OpenApiResponse(
            description="Неверные параметры запроса",
            response=PartnerErrorResponseSerializer,
        ),
    },
)
