from rest_framework import serializers

from api.models import Policy


class PolicySerializer(serializers.ModelSerializer):
    """Сериализатор для отображения юр. страниц."""

    class Meta:
        model = Policy
        fields = ("id", "header", "text", "slug")
