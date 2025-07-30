from rest_framework import serializers

from api.models import Partner


class PartnerSerializer(serializers.ModelSerializer):
    """Сериализатор для получения партнеров."""

    class Meta:
        model = Partner
        fields = ("id", "name", "logo", "website")
