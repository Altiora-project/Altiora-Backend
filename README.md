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

## Установка виртуального окружения и зависимостей

```bash
python -m venv venv
```

```bash
source venv/bin/activate
```

```bash
python -m pip install --upgrade pip
```

Установка зависимостей
```bash
pip install -r backend/requirements.txt
```

Установка зависимостей для разработки
```bash
pip install -r backend/requirements-dev.txt
```

## Запуск инфраструктуры

### Полная локальная инфраструктура (PostgreSQL + RabbitMQ + Celery)

Запуск всех необходимых сервисов для разработки:

```bash
sudo docker compose -f docker-compose.local.yml up --build
```

Этот compose файл включает:
- **PostgreSQL** (порт 5433) - база данных
- **RabbitMQ** (порты 5672, 15672) - брокер сообщений для Celery
- **Celery Worker** - обработчик асинхронных задач

RabbitMQ Management UI будет доступен по адресу: http://localhost:15672
- Логин: `user`
- Пароль: `pass`

В .env файле нужно указать:
```bash
# для полной инфраструктуры в контейнерах
POSTGRES_HOST=localhost
CELERY_BROKER_URL=amqp://user:pass@localhost:5672//
RABBITMQ_DEFAULT_USER=user
RABBITMQ_DEFAULT_PASS=pass
```

### Локальный запуск только PostgreSQL в контейнере

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

