from http import HTTPStatus

from drf_spectacular.utils import OpenApiResponse, extend_schema

from api.serializers import (
    ProjectRequestErrorResponseSerializer,
    ProjectRequestResponseSerializer,
    ProjectRequestSerializer,
)


project_request_create_schema = extend_schema(
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
