from api.serializers.models.services import (
    ServiceListSerializer,
    ServiceDetailSerializer,
    ServiceDetailDocSerializer,
)
from api.serializers.responses.base import (
    BaseResponseSerializer,
    ErrorResponseSerializer,
)


class ServiceListResponseSerializer(BaseResponseSerializer):
    """
    Сериализатор для ответа с данными о списке услуг и проектов.
    Используется в т.ч. для Swagger.
    """

    data = ServiceListSerializer()


class ServiceDetailResponseSerializer(BaseResponseSerializer):
    """Сериализатор для получения услуги."""

    data = ServiceDetailSerializer()


class ServiceDetailDocResponseSerializer(BaseResponseSerializer):
    """Сериализатор для документации Swagger детального просмотра услуги."""

    data = ServiceDetailDocSerializer()


class ServiceErrorResponseSerializer(ErrorResponseSerializer):
    """Сериализатор для ответа с ошибками при получении услуг."""

    pass
