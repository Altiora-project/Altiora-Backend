NAME_MAX_LENGTH = 255
INFO_MAX_LENGTH = 2000
TEXT_MAX_LENGTH = 1000

CARD_CHOICES_MAX_LENGTH = 25
CARD_CHOICES = {
    "startup_laboratory": "startup",
    "startup_laboratory_text": "Лаборатория стартапов",
    "digital_marketing": "digital",
    "digital_marketing_text": "Digital маркетинг",
}

API_VERSION = "v1"

# Настройки для админки
ADMIN_SITE_TITLE = "Altiora Website Admin"
ADMIN_SITE_HEADER = "Панель управления Altiora Website"
ADMIN_INDEX_TITLE = "Добро пожаловать в админку Altiora Website"


# Настройки для robots.txt
ROBOTS_TXT_TEMPLATE = """User-agent: *
Disallow: /admin/
Disallow: /api/
Disallow: /static/
Disallow: /media/
Disallow: /auth/
Disallow: /accounts/
Sitemap: {scheme}://{host}/sitemap.xml
"""

# Настройки для Telegram
API_URL = "https://api.telegram.org/bot{BOT_TOKEN}"

TELEGRAM_NOTIFICATION_TEMPLATE = """
‼️<b><u>Новая заявка от {name}</u></b>\n
<b>👤 Имя:</b> {name}
<b>🏢 Компания:</b> {company}
<b>📞 Телефон:</b> {phone_number}
<b>📧 Email:</b> {email}
<b>📝 Детали проекта:</b> {project_details}
"""
