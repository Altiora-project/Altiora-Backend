from rest_framework import serializers

from api.models import LegalPage


class LegalPageSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения юр. страниц."""

    class Meta:
        model = LegalPage
        fields = (
            "id",
            "header",
            "text",
            "slug"
        )
