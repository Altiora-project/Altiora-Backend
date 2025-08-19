# Model сериализаторы
from api.serializers.models import (
    # Главная страница
    HomePageContentSerializer,
    # Партнеры
    PartnerSerializer,
    # Заявки на проект
    ProjectRequestSerializer,
    # Технологии
    TechnologySerializer,
    # Услуги
    CaseStudySerializer,
    ServiceDetailDocSerializer,
    ServiceDetailSerializer,
    ServiceListSerializer,
    ServiceListSimpleSerializer,
    ServicePostscriptumSerializer,
    # Теги
    TagSerializer,
    # Статика
    SiteSettingsSerializer,
)

# Response сериализаторы
from api.serializers.responses import (
    # Базовые
    BaseResponseSerializer,
    ErrorResponseSerializer,
    # Главная страница
    HomePageContentErrorResponseSerializer,
    HomePageContentResponseSerializer,
    # Партнеры
    PartnerErrorResponseSerializer,
    PartnerResponseSerializer,
    # Заявки на проект
    ProjectRequestErrorResponseSerializer,
    ProjectRequestResponseSerializer,
    # Технологии
    TechnologyErrorResponseSerializer,
    TechnologyListResponseSerializer,
    TechnologyResponseSerializer,
    # Услуги
    ServiceDetailDocResponseSerializer,
    ServiceDetailResponseSerializer,
    ServiceErrorResponseSerializer,
    ServiceListResponseSerializer,
    # Статика
    SiteSettingsResponseSerializer,
    SiteSettingsErrorResponseSerializer,
)

# flake8: noqa
# ruff: noqa
