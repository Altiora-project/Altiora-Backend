import re

from rest_framework import serializers

from .models import ProjectRequest


class BaseResponseSerializer(serializers.Serializer):
    """Базовый сериализатор для успешных ответов."""
    success = serializers.BooleanField(
        help_text='Статус успешности операции',
        default=True
    )
    message = serializers.CharField(
        help_text='Сообщение об операции'
    )
    data = serializers.JSONField(
        help_text='Данные операции',
        required=False
    )


class ErrorResponseSerializer(serializers.Serializer):
    """Сериализатор для ответов с ошибками."""
    success = serializers.BooleanField(
        help_text='Статус успешности операции',
        default=False
    )
    message = serializers.CharField(
        help_text='Сообщение об ошибке'
    )
    errors = serializers.DictField(
        child=serializers.ListField(
            child=serializers.CharField(),
            help_text='Список ошибок для конкретного поля'
        ),
        help_text='Словарь ошибок валидации, где ключ - название поля, '
                  'значение - список ошибок',
        required=False,
        allow_empty=True
    )


class ProjectRequestSerializer(serializers.ModelSerializer):
    """
    Сериализатор заявки на проект.
    Валидация телефона и согласия с условиями.
    """

    name = serializers.CharField(
        help_text="Имя клиента, отправившего заявку."
    )
    company = serializers.CharField(
        help_text="Название компании клиента."
    )
    project_details = serializers.CharField(
        help_text="Описание проекта или задачи, которую нужно реализовать."
    )
    phone_number = serializers.CharField(
        help_text="Контактный номер телефона в формате +79991234567."
    )
    email = serializers.EmailField(
        help_text="Электронная почта для связи."
    )
    agreed_to_terms = serializers.BooleanField(
        help_text="Флаг подтверждения согласия с политикой обработки "
        "персональных данных."
    )

    class Meta:
        model = ProjectRequest
        fields = [
            'name',
            'company',
            'project_details',
            'phone_number',
            'email',
            'agreed_to_terms',
        ]
        read_only_fields = ['created_at']

    def validate_phone_number(self, value):
        """Проверка формата номера телефона."""
        pattern = r'^\+?[1-9]\d{1,14}$'
        if not re.match(pattern, value):
            raise serializers.ValidationError(
                'Неверный формат номера телефона. '
                'Пожалуйста, используйте формат +79991234567'
            )
        return value

    def validate_agreed_to_terms(self, value):
        """Проверка согласия с условиями обработки персональных данных."""
        if value is not True:
            raise serializers.ValidationError(
                'Необходимо согласиться с политикой обработки '
                'персональных данных.'
            )
        return value


class ProjectRequestResponseSerializer(BaseResponseSerializer):
    """Сериализатор для ответа при создании заявки на проект."""
    data = ProjectRequestSerializer()


class ProjectRequestErrorResponseSerializer(ErrorResponseSerializer):
    """Сериализатор для ответа с ошибками при создании заявки на проект."""
    pass
