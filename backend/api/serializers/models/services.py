from rest_framework import serializers

from api.models import CaseStudy, Service, ServicePostscriptum
from api.serializers.models.tags import TagSerializer


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
            "slug",
            "content",
            "tags",
        )


class ServiceListSerializer(serializers.Serializer):
    """Сериализатор для полного списка услуг и проектов."""

    services = ServiceListSimpleSerializer(many=True, help_text="Список услуг")
    case_studies = CaseStudySerializer(many=True, help_text="Список проектов")


SERVICE_DETAIL_FIELDS = (
    "id",
    "number",
    "name",
    "slug",
    "content",
    "tags",
    "postscriptum",
    "case_studies",
    "meta_title",
    "meta_description",
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
        many=True,
        read_only=True,
        help_text="Список проектов",
    )

    class Meta:
        model = Service
        fields = SERVICE_DETAIL_FIELDS
