from api.serializers.models.partners import PartnerSerializer
from api.serializers.responses.base import (
    BaseResponseSerializer,
    ErrorResponseSerializer,
)


class PartnerResponseSerializer(BaseResponseSerializer):
    """Сериализатор для ответа на запрос партнеров."""

    data = PartnerSerializer(many=True)


class PartnerErrorResponseSerializer(ErrorResponseSerializer):
    """Сериализатор для ответа с ошибками при получении партнеров."""

    pass
