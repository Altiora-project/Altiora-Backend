import re

from rest_framework import serializers

from .models import (
    ProjectRequest,
    Technology,
    Service,
    Tag,
    ServicePostscriptum,
    CaseStudy,
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


class ServiceListSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения услуг в списке.
    Не включает поле content для экономии трафика.
    """

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
        fields = (
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

    def get_postscriptum(self, obj):
        """Получает данные постскриптума услуги."""
        try:
            postscriptum = ServicePostscriptum.objects.first()
            if postscriptum:
                return ServicePostscriptumSerializer(postscriptum).data
            return None
        except ServicePostscriptum.DoesNotExist:
            return None


class ServiceResponseSerializer(BaseResponseSerializer):
    """Сериализатор для получения услуги."""

    data = ServiceDetailSerializer()


class ServiceListResponseSerializer(BaseResponseSerializer):
    """Сериализатор для получения списка услуг."""

    data = ServiceListSerializer(many=True)


class ServiceListWithCaseStudiesResponseSerializer(BaseResponseSerializer):
    """Сериализатор для получения списка услуг с реальными проектами."""

    data = serializers.DictField(
        child=serializers.JSONField(), help_text="Данные услуг и проектов"
    )


class ServiceListWCSDataSerializer(serializers.Serializer):
    """Сериализатор для данных услуг и проектов в ответе."""

    services = ServiceListSerializer(many=True, help_text="Список услуг")
    case_studies = CaseStudySerializer(many=True, help_text="Список проектов")


class ServiceListWCSSwaggerResponseSerializer(BaseResponseSerializer):
    """Сериализатор для документации Swagger."""

    data = ServiceListWCSDataSerializer()


class ServiceErrorResponseSerializer(ErrorResponseSerializer):
    """Сериализатор для ответа с ошибками при получении услуг."""

    pass


class ServiceDetailSwaggerSerializer(serializers.ModelSerializer):
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
        fields = (
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


class ServiceDetailSwaggerResponseSerializer(BaseResponseSerializer):
    """Сериализатор для документации Swagger детального просмотра услуги."""

    data = ServiceDetailSwaggerSerializer()
