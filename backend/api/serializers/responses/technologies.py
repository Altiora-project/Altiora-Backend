from api.serializers.models.technologies import TechnologySerializer
from api.serializers.responses.base import (
    BaseResponseSerializer,
    ErrorResponseSerializer,
)


class TechnologyResponseSerializer(BaseResponseSerializer):
    """Сериализатор для получения технологии."""

    data = TechnologySerializer()


class TechnologyListResponseSerializer(BaseResponseSerializer):
    """Сериализатор для получения списка технологий."""

    data = TechnologySerializer(many=True)


class TechnologyErrorResponseSerializer(ErrorResponseSerializer):
    """Сериализатор для ответа с ошибками при получении технологий."""

    pass
