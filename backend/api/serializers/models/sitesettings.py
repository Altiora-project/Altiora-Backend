from rest_framework import serializers

from api.models import SiteSettings


class SiteSettingsSerializer(serializers.ModelSerializer):
    """Сериализатор статики сайта."""

    logo_url = serializers.SerializerMethodField()

    def get_logo_url(self, obj):
        """Получаем URL изображения logo."""
        request = self.context.get("request")
        if obj.logo and hasattr(obj.logo, "url"):
            return request.build_absolute_uri(obj.logo.url)
        return None

    class Meta:
        model = SiteSettings
        fields = ("logo_url", "phone", "email", "address", "requisites")
