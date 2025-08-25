import re

from rest_framework import serializers

from api.models import ProjectRequest


class ProjectRequestSerializer(serializers.ModelSerializer):
    """
    Сериализатор заявки на проект.
    Валидация телефона и согласия с условиями.
    """

    name = serializers.CharField(
        help_text="Имя клиента, отправившего заявку.", max_length=255
    )
    company = serializers.CharField(
        help_text="Название компании клиента.", max_length=255
    )
    project_details = serializers.CharField(
        help_text="Описание проекта или задачи, которую нужно реализовать."
    )
    phone_number = serializers.CharField(
        help_text="Контактный номер телефона в формате +79991234567."
    )
    email = serializers.EmailField(
        help_text="Электронная почта для связи.", max_length=255
    )
    agreed_to_terms = serializers.BooleanField(
        help_text="Флаг подтверждения согласия с политикой обработки "
        "персональных данных."
    )

    class Meta:
        model = ProjectRequest
        fields = [
            "name",
            "company",
            "project_details",
            "phone_number",
            "email",
            "agreed_to_terms",
        ]
        read_only_fields = ["created_at"]

    def validate_phone_number(self, value):
        """Проверка формата номера телефона."""
        pattern = r"^\+?[1-9]\d{1,14}$"
        if not re.match(pattern, value):
            raise serializers.ValidationError(
                "Неверный формат номера телефона. "
                "Пожалуйста, используйте формат +79991234567"
            )
        return value

    def validate_agreed_to_terms(self, value):
        """Проверка согласия с условиями обработки персональных данных."""
        if value is not True:
            raise serializers.ValidationError(
                "Необходимо согласиться с политикой обработки "
                "персональных данных."
            )
        return value
