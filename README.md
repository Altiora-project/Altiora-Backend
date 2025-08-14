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
- **PostgreSQL** (порт 5432) - база данных
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

### Добавление тестовых данных (фикстур)

```bash
python manage.py loaddata fixtures/<name_of_fixture.json>
```

Список фикстур:

- `casestudy.json`
- `homepagecontent.json`
- `labcart.json`
- `partner.json`
- `service.json`
- `servicepostscriptum.json`
- `sitesettings.json`
- `tag.json`
- `technology.json`



## Доступ к админке Django

Для обеспечения безопасности админка Django защищена middleware с использованием хеша в URL.

### Настройка доступа

1. **Установите переменную окружения `ADMIN_HASH`:**
   ```bash
   # В файле .env добавьте:
   ADMIN_HASH=your_secure_hash_here
   ```

2. **Создайте безопасный хеш:**
   ```bash
   # Пример генерации хеша (используйте любой метод):
   echo -n "your_secret_password" | sha256sum
   # или
   openssl rand -hex 32
   ```

### Доступ к админке

1. **Первый доступ (активация сессии):**
   ```
   http://localhost:8000/admin/YOUR_ADMIN_HASH/
   ```
   
   Если хеш корректный, вы будете перенаправлены на:
   ```
   http://localhost:8000/admin/
   ```

2. **Последующие доступы:**
   После успешной активации сессии вы можете использовать обычный URL:
   ```
   http://localhost:8000/admin/
   ```

### Безопасность

- Сессия истекает при закрытии браузера (`SESSION_EXPIRE_AT_BROWSER_CLOSE = True`)
- Прямой доступ к `/admin/` без хеша заблокирован
- Неверный хеш возвращает ошибку 404
- Хеш должен храниться в переменной окружения `ADMIN_HASH`

### Пример использования

```bash
# В .env файле:
ADMIN_HASH=a1b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456

# Доступ к админке:
# http://localhost:8000/admin/a1b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456/
```
