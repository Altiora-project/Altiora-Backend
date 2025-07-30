from api.serializers.models.project_request import ProjectRequestSerializer
from api.serializers.responses.base import (
    BaseResponseSerializer,
    ErrorResponseSerializer,
)


class ProjectRequestResponseSerializer(BaseResponseSerializer):
    """Сериализатор для ответа при создании заявки на проект."""

    data = ProjectRequestSerializer()


class ProjectRequestErrorResponseSerializer(ErrorResponseSerializer):
    """Сериализатор для ответа с ошибками при создании заявки на проект."""

    pass
