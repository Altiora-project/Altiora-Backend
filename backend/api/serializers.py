import re

from rest_framework import serializers

from .models import (
    CaseStudy,
    HomePageContent,
    Partner,
    ProjectRequest,
    Service,
    ServicePostscriptum,
    Tag,
    Technology,
)


class BaseResponseSerializer(serializers.Serializer):
    """Базовый сериализатор для успешных ответов."""

    success = serializers.BooleanField(
        help_text="Статус успешности операции", default=True
    )
    message = serializers.CharField(help_text="Сообщение об операции")
    data = serializers.JSONField(help_text="Данные операции", required=False)


class ErrorResponseSerializer(serializers.Serializer):
    """Сериализатор для ответов с ошибками."""

    success = serializers.BooleanField(
        help_text="Статус успешности операции", default=False
    )
    message = serializers.CharField(help_text="Сообщение об ошибке")
    errors = serializers.DictField(
        child=serializers.ListField(
            child=serializers.CharField(),
            help_text="Список ошибок для конкретного поля",
        ),
        help_text="Словарь ошибок валидации, где ключ - название поля, "
        "значение - список ошибок",
        required=False,
        allow_empty=True,
    )


class ProjectRequestSerializer(serializers.ModelSerializer):
    """
    Сериализатор заявки на проект.
    Валидация телефона и согласия с условиями.
    """

    name = serializers.CharField(help_text="Имя клиента, отправившего заявку.")
    company = serializers.CharField(help_text="Название компании клиента.")
    project_details = serializers.CharField(
        help_text="Описание проекта или задачи, которую нужно реализовать."
    )
    phone_number = serializers.CharField(
        help_text="Контактный номер телефона в формате +79991234567."
    )
    email = serializers.EmailField(help_text="Электронная почта для связи.")
    agreed_to_terms = serializers.BooleanField(
        help_text="Флаг подтверждения согласия с политикой обработки "
        "персональных данных."
    )

    class Meta:
        model = ProjectRequest
        fields = [
            "name",
            "company",
            "project_details",
            "phone_number",
            "email",
            "agreed_to_terms",
        ]
        read_only_fields = ["created_at"]

    def validate_phone_number(self, value):
        """Проверка формата номера телефона."""
        pattern = r"^\+?[1-9]\d{1,14}$"
        if not re.match(pattern, value):
            raise serializers.ValidationError(
                "Неверный формат номера телефона. "
                "Пожалуйста, используйте формат +79991234567"
            )
        return value

    def validate_agreed_to_terms(self, value):
        """Проверка согласия с условиями обработки персональных данных."""
        if value is not True:
            raise serializers.ValidationError(
                "Необходимо согласиться с политикой обработки "
                "персональных данных."
            )
        return value


class ProjectRequestResponseSerializer(BaseResponseSerializer):
    """Сериализатор для ответа при создании заявки на проект."""

    data = ProjectRequestSerializer()


class ProjectRequestErrorResponseSerializer(ErrorResponseSerializer):
    """Сериализатор для ответа с ошибками при создании заявки на проект."""

    pass


class TechnologySerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения технологий.
    Относится к странице Лаборатория стартапов.
    """

    class Meta:
        model = Technology
        fields = (
            "id",
            "number",
            "name",
            "primary_info",
            "secondary_info",
            "image",
        )


class TechnologyResponseSerializer(BaseResponseSerializer):
    """Сериализатор для получения технологии."""

    data = TechnologySerializer()


class TechnologyListResponseSerializer(BaseResponseSerializer):
    """Сериализатор для получения списка технологий."""

    data = TechnologySerializer(many=True)


class TechnologyErrorResponseSerializer(ErrorResponseSerializer):
    """Сериализатор для ответа с ошибками при получении технологий."""

    pass


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения тегов."""

    class Meta:
        model = Tag
        fields = ("id", "name")


class ServicePostscriptumSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения постскриптума услуги."""

    class Meta:
        model = ServicePostscriptum
        fields = (
            "id",
            "name",
            "info",
            "item1",
            "item2",
            "item3",
            "item4",
        )


class CaseStudySerializer(serializers.ModelSerializer):
    """Сериализатор для отображения реальных проектов."""

    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = CaseStudy
        fields = (
            "id",
            "name",
            "info",
            "tags",
        )


class ServiceListSimpleSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения услуг в простом формате в списке."""

    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Service
        fields = (
            "id",
            "number",
            "name",
            "info",
            "tags",
        )


class ServiceListSerializer(serializers.Serializer):
    """Сериализатор для полного списка услуг и проектов."""

    services = ServiceListSimpleSerializer(many=True, help_text="Список услуг")
    case_studies = CaseStudySerializer(many=True, help_text="Список проектов")


class ServiceListResponseSerializer(BaseResponseSerializer):
    """
    Сериализатор для ответа с данными о списке услуг и проектов.
    Используется в т.ч. для Swagger.
    """

    data = ServiceListSerializer()


SERVICE_DETAIL_FIELDS = (
    "id",
    "number",
    "name",
    "info",
    "content",
    "tags",
    "postscriptum",
    "case_studies",
    "seo_title",
    "seo_description",
)


class ServiceDetailSerializer(serializers.ModelSerializer):
    """
    Сериализатор для детального отображения услуги.
    Включает все поля, включая content, postscriptum и case_studies.
    """

    tags = TagSerializer(many=True, read_only=True)
    postscriptum = serializers.SerializerMethodField()
    case_studies = CaseStudySerializer(many=True, read_only=True)

    class Meta:
        model = Service
        fields = SERVICE_DETAIL_FIELDS

    def get_postscriptum(self, obj):
        """Получает данные постскриптума услуги."""
        try:
            postscriptum = ServicePostscriptum.objects.first()
            if postscriptum:
                return ServicePostscriptumSerializer(postscriptum).data
            return None
        except ServicePostscriptum.DoesNotExist:
            return None


class ServiceDetailResponseSerializer(BaseResponseSerializer):
    """Сериализатор для получения услуги."""

    data = ServiceDetailSerializer()


class ServiceDetailDocSerializer(serializers.ModelSerializer):
    """
    Сериализатор для документации Swagger детального просмотра услуги.
    Явно определяет структуру всех полей для корректного отображения в Swagger.
    """

    tags = TagSerializer(many=True, read_only=True)
    postscriptum = ServicePostscriptumSerializer(
        help_text="Данные постскриптума услуги"
    )
    case_studies = CaseStudySerializer(
        many=True, read_only=True, help_text="Список проектов"
    )

    class Meta:
        model = Service
        fields = SERVICE_DETAIL_FIELDS


class ServiceDetailDocResponseSerializer(BaseResponseSerializer):
    """Сериализатор для документации Swagger детального просмотра услуги."""

    data = ServiceDetailDocSerializer()


class ServiceErrorResponseSerializer(ErrorResponseSerializer):
    """Сериализатор для ответа с ошибками при получении услуг."""

    pass


class PartnerSerializer(serializers.ModelSerializer):
    """Сериализатор для получения партнеров."""

    class Meta:
        model = Partner
        fields = ("id", "name", "logo", "website")


class PartnerResponseSerializer(BaseResponseSerializer):
    """Сериализатор для ответа на запрос партнеров."""

    data = PartnerSerializer()


class PartnerErrorResponseSerializer(ErrorResponseSerializer):
    """Сериализатор для ответа с ошибками при получении партнеров."""

    pass


class HomePageContentSerializer(serializers.ModelSerializer):
    """Сериализатор для главной страницы."""

    partners_data = PartnerSerializer(many=True, read_only=True)
    services_data = ServiceListSimpleSerializer(many=True, read_only=True)

    class Meta:
        model = HomePageContent
        fields = [
            "meta_title",
            "meta_description",
            "hero_title",
            "hero_subtitle",
            "hero_image",
            "about_title",
            "about_text",
            "higlight_1",
            "higlight_2",
            "services_section_title",
            "lab_title",
            "lab_description",
            "dig_title",
            "dig_description",
            "tokenization_title",
            "tokenization_description",
            "tokenization_video_url",
            "tokenization_links",
            "partners_section_title",
            "partners_data",
            "services_data",
            "order_section_title",
            "contacts_title",
            "contact_address",
            "contact_phone",
            "contact_email",
        ]

    def to_representation(self, instance):
        """Переопределяем для добавления partners_data."""
        data = super().to_representation(instance)
        partners_data = Partner.objects.all()
        services_data = Service.objects.all()
        data["partners_data"] = PartnerSerializer(
            partners_data, many=True
        ).data
        data["services_data"] = ServiceListSimpleSerializer(
            services_data, many=True
        ).data
        return data


class HomePageContentResponseSerializer(BaseResponseSerializer):
    """Сериализатор для ответа главной страницы."""

    data = HomePageContentSerializer()


class HomePageContentErrorResponseSerializer(ErrorResponseSerializer):
    """Сериализатор для ответа с ошибками главной страницы."""

    pass
