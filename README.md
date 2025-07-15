# Altiora-Backend

## Структура проекта

```bash
backend/ # Проект Django
│ ├── manage.py
│ ├── altiora_backend/ # Основная конфигурация Django
│ │ ├── init.py
│ │ ├── settings.py
│ │ ├── urls.py
│ │ ├── wsgi.py
│ │ └── asgi.py
│ ├── api/ # Приложение Django для вашего API
│ │ ├── init.py
│ │ ├── admin.py
│ │ ├── apps.py
│ │ ├── migrations/
│ │ ├── models.py # Здесь будут ваши модели данных
│ │ ├── serializers.py # Сериализаторы для DRF
│ │ ├── tests.py
│ │ ├── urls.py # URL-адреса для API
│ │ └── views.py # Представления для API (APIView, ViewSet)
│ ├── media/ # Медиафайлы (загруженные пользователями)
│ ├── static/ # Общие статические файлы для Django
│ └── requirements.txt # Зависимости Python
```

## Локальный запуск только postgres в контейнере

```bash
sudo docker compose -f docker-compose.local.postgres.yml up --build
```

В .env файле нужно указать:
```bash
# для запуска только postgres в контейнере
POSTGRES_HOST=localhost
```

## Запуск Django server

```bash
cd backend/
```

```bash
python manage.py migrate
```

```bash
python manage.py createsuperuser
```

```bash
python manage.py runserver 8000
```

