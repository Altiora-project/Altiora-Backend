from api.serializers.models.homepage import HomePageContentSerializer
from api.serializers.responses.base import (
    BaseResponseSerializer,
    ErrorResponseSerializer,
)


class HomePageContentResponseSerializer(BaseResponseSerializer):
    """Сериализатор для ответа главной страницы."""

    data = HomePageContentSerializer()


class HomePageContentErrorResponseSerializer(ErrorResponseSerializer):
    """Сериализатор для ответа с ошибками главной страницы."""

    pass
