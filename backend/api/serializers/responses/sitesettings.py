from api.serializers.models.sitesettings import SiteSettingsSerializer
from api.serializers.responses.base import (
    BaseResponseSerializer,
    ErrorResponseSerializer,
)


class SiteSettingsResponseSerializer(BaseResponseSerializer):
    """Сериализатор для ответа статики."""

    data = SiteSettingsSerializer()


class SiteSettingsErrorResponseSerializer(ErrorResponseSerializer):
    """Сериализатор для ответа с ошибками статики."""

    pass
