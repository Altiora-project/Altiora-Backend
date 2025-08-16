from api.serializers import PolicySerializer
from api.serializers.responses.base import (
    BaseResponseSerializer,
    ErrorResponseSerializer,
)


class PolicyResponseSerializer(BaseResponseSerializer):
    """Сериализатор для получения юридической страницы."""

    data = PolicySerializer()


class PolicyListResponseSerializer(BaseResponseSerializer):
    """Сериализатор для получения списка юридических страниц."""

    data = PolicySerializer(many=True)


class PolicyErrorResponseSerializer(ErrorResponseSerializer):
    """Сериализатор для ответа с ошибками при получении юридических страниц."""

    pass
