from backend.api.serializers.models.policy import Policy
from api.serializers.responses.base import (
    BaseResponseSerializer,
    ErrorResponseSerializer,
)


class PolicyResponseSerializer(BaseResponseSerializer):
    """Сериализатор для получения юридической страницы."""

    data = Policy()


class PolicyListResponseSerializer(BaseResponseSerializer):
    """Сериализатор для получения списка юридических страниц."""

    data = Policy(many=True)


class PolicyErrorResponseSerializer(ErrorResponseSerializer):
    """Сериализатор для ответа с ошибками при получении юридических страниц."""

    pass
