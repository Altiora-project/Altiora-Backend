from rest_framework import serializers

from api.models import Tag


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения тегов."""

    class Meta:
        model = Tag
        fields = ("id", "name")
