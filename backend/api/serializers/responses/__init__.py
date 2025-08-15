# Базовые response сериализаторы
from api.serializers.responses.base import (
    BaseResponseSerializer,
    ErrorResponseSerializer,
)

# Response сериализаторы главной страницы
from api.serializers.responses.homepage import (
    HomePageContentErrorResponseSerializer,
    HomePageContentResponseSerializer,
)

# Response сериализаторы партнеров
from api.serializers.responses.partners import (
    PartnerErrorResponseSerializer,
    PartnerResponseSerializer,
)

# Response сериализаторы заявок на проект
from api.serializers.responses.project_request import (
    ProjectRequestErrorResponseSerializer,
    ProjectRequestResponseSerializer,
)

# Response сериализаторы технологий
from api.serializers.responses.technologies import (
    TechnologyErrorResponseSerializer,
    TechnologyListResponseSerializer,
    TechnologyResponseSerializer,
)

# Response сериализаторы услуг
from api.serializers.responses.services import (
    ServiceDetailDocResponseSerializer,
    ServiceDetailResponseSerializer,
    ServiceErrorResponseSerializer,
    ServiceListResponseSerializer,
)

# Response сериализаторы статики
from api.serializers.responses.sitesettings import (
    SiteSettingsResponseSerializer,
    SiteSettingsErrorResponseSerializer,
)

# Response сериализаторы юридических страниц
from backend.api.serializers.responses.policy import (
    PolicyResponseSerializer,
    PolicyListResponseSerializer,
    PolicyErrorResponseSerializer,
)

# flake8: noqa
# ruff: noqa
