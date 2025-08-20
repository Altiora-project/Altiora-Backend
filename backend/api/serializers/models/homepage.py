from api.models import CaseStudy, HomePageContent, LabCart, Partner, Service
from api.serializers.models.labcarts import LabCartSerializer
from api.serializers.models.partners import PartnerSerializer
from api.serializers.models.services import (
    CaseStudySerializer,
    ServiceListSimpleSerializer,
)
from rest_framework import serializers


class HomePageContentSerializer(serializers.ModelSerializer):
    """Сериализатор для главной страницы."""

    partners_data = PartnerSerializer(many=True, read_only=True)
    services_running_line = serializers.SerializerMethodField()
    services_data = ServiceListSimpleSerializer(many=True, read_only=True)
    case_studies_data = CaseStudySerializer(many=True, read_only=True)
    hero_image = serializers.SerializerMethodField()
    labcart_data = LabCartSerializer(many=True, read_only=True)

    def get_hero_image(self, obj):
        """Получаем URL изображения hero_image."""
        if not hasattr(obj, "hero_image") or not obj.hero_image:
            return None
        request = self.context.get("request")
        try:
            url = obj.hero_image.url
            return request.build_absolute_uri(url) if request else url
        except Exception:
            return None

    def get_services_running_line(self, obj):
        """Возвращаем список названий всех услуг."""
        return list(Service.objects.values_list("name", flat=True))

    class Meta:
        model = HomePageContent
        fields = [
            "meta_title",
            "meta_description",
            "hero_title",
            "hero_subtitle",
            "hero_image",
            "services_running_line",
            "about_title",
            "about_text",
            "highlight_1",
            "highlight_2",
            "services_section_title",
            "services_section_description",
            "lab_title",
            "lab_description",
            "labcart_data",
            "lab_description_ps",
            "dig_title",
            "dig_description",
            "tokenization_title",
            "tokenization_description",
            "tokenization_video_url",
            "tokenization_links",
            "partners_section_title",
            "partners_data",
            "services_data",
            "case_studies_data",
            "order_section_title",
            "contacts_title",
            "contact_address",
            "contact_phone",
            "contact_email",
        ]

    def to_representation(self, instance):
        """Переопределяем для добавления partners_data."""
        data = super().to_representation(instance)
        labcart_data = LabCart.objects.all()
        partners_data = Partner.objects.all()
        services_data = Service.objects.all()
        case_studies_data = CaseStudy.objects.all()
        data["labcart_data"] = LabCartSerializer(labcart_data, many=True).data
        data["partners_data"] = PartnerSerializer(
            partners_data, many=True
        ).data
        data["services_data"] = ServiceListSimpleSerializer(
            services_data, many=True
        ).data
        data["case_studies_data"] = CaseStudySerializer(
            case_studies_data, many=True
        ).data
        return data
