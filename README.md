# Altiora-Backend

## Проверка flake8 и black

Проверка PEP8
```bash
flake8 backend/
```

Проверка кода
```bash
black --check backend/
```

Форматирование кода
```bash
black {source_file_or_directory}
```


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
CELERY_HOST=localhost
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

### Настройка переменных окружения

Скопируйте файл `env_example` в `.env` и настройте переменные:

```bash
cp env_example .env
```

**Для локальной разработки с полной инфраструктурой (PostgreSQL + RabbitMQ + Celery):**
```bash
POSTGRES_HOST=localhost
CELERY_HOST=localhost
RABBITMQ_DEFAULT_USER=user
RABBITMQ_DEFAULT_PASS=pass
```

**Для локальной разработки только с PostgreSQL:**
```bash
POSTGRES_HOST=localhost
# Celery и RabbitMQ не используются
```

**Для Docker окружения:**
```bash
POSTGRES_HOST=postgres
CELERY_HOST=rabbitmq
RABBITMQ_DEFAULT_USER=user
RABBITMQ_DEFAULT_PASS=pass
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

