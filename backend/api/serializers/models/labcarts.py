from api.models import LabCart
from rest_framework import serializers


class LabCartSerializer(serializers.ModelSerializer):
    """Сериализатор карточки лаборатории стартапов."""

    class Meta:
        model = LabCart
        fields = ("id", "title", "image", "description")
