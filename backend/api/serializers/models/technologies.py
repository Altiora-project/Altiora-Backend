from rest_framework import serializers

from api.models import Technology


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
