from api.serializers.models.legalpage import LegalPage
from api.serializers.responses.base import (
    BaseResponseSerializer,
    ErrorResponseSerializer,
)


class LegalPageResponseSerializer(BaseResponseSerializer):
    """Сериализатор для получения технологии."""

    data = LegalPage()


class LegalPageListResponseSerializer(BaseResponseSerializer):
    """Сериализатор для получения списка технологий."""

    data = LegalPage(many=True)


class LegalPageErrorResponseSerializer(ErrorResponseSerializer):
    """Сериализатор для ответа с ошибками при получении технологий."""

    pass
