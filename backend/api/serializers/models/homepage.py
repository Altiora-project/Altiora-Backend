from rest_framework import serializers

from api.models import HomePageContent, Partner, Service
from api.serializers.models.partners import PartnerSerializer
from api.serializers.models.services import ServiceListSimpleSerializer


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
            "highlight_1",
            "highlight_2",
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
