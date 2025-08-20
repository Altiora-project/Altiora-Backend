# Model сериализаторы главной страницы
from api.serializers.models.homepage import HomePageContentSerializer

# Model сериализаторы партнеров
from api.serializers.models.partners import PartnerSerializer

# Model сериализаторы заявок на проект
from api.serializers.models.project_request import ProjectRequestSerializer

# Model сериализаторы технологий
from api.serializers.models.technologies import TechnologySerializer

# Model сериализаторы услуг
from api.serializers.models.services import (
    CaseStudySerializer,
    ServiceDetailDocSerializer,
    ServiceDetailSerializer,
    ServiceListSerializer,
    ServiceListSimpleSerializer,
    ServicePostscriptumSerializer,
    ServicesRunningLineSerializer,
)

# Model сериализатор статики сайта
from api.serializers.models.sitesettings import SiteSettingsSerializer

# Model сериализаторы тегов
from api.serializers.models.tags import TagSerializer

# Model сериализатор юридических страниц
from api.serializers.models.policy import PolicySerializer

# flake8: noqa
# ruff: noqa
