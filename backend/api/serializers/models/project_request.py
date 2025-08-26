import re

from rest_framework import serializers

from api.models import ProjectRequest
from altiora_backend import constants


class ProjectRequestSerializer(serializers.ModelSerializer):
    """
    Сериализатор заявки на проект.
    Валидация телефона и согласия с условиями.
    """

    name = serializers.CharField(
        help_text="Имя клиента, отправившего заявку.",
        max_length=constants.NAME_MAX_LENGTH,
    )
    company = serializers.CharField(
        help_text="Название компании клиента.",
        max_length=constants.NAME_MAX_LENGTH,
    )
    project_details = serializers.CharField(
        help_text="Описание проекта или задачи, которую нужно реализовать.",
        max_length=constants.PROJECT_DETAILS_MAX_LENGTH,
    )
    phone_number = serializers.CharField(
        help_text="Контактный номер телефона в формате +79991234567.",
        max_length=constants.PHONE_NUMBER_MAX_LENGTH,
    )
    email = serializers.EmailField(
        help_text="Электронная почта для связи.",
        max_length=constants.EMAIL_MAX_LENGTH,
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
