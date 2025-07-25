#!/bin/bash
set -e

if [ ! -d "./api/migrations" ]; then
  echo "Папка api/migrations не найдена. Создаём..."
  mkdir -p ./api/migrations
fi

# Убедимся, что в ней есть __init__.py
if [ ! -f "./api/migrations/__init__.py" ]; then
  echo "Добавляем __init__.py в migrations..."
  touch ./api/migrations/__init__.py
fi

echo "Создаём миграции..."
python manage.py makemigrations --noinput

echo "Применяем миграции..."
python manage.py migrate --noinput

echo "Собираем статику..."
python manage.py collectstatic --noinput

echo "Создаём суперпользователя, если он ещё не существует..."
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
import os

User = get_user_model()
username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin")
email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "adminpass")

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"Суперпользователь '{username}' создан.")
else:
    print(f"Суперпользователь '{username}' уже существует.")
EOF

echo "Миграции и статика применены. Запускаем: $@"
exec "$@"
