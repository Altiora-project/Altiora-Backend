NAME_MAX_LENGTH = 255
INFO_MAX_LENGTH = 2000
TEXT_MAX_LENGTH = 1000

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
