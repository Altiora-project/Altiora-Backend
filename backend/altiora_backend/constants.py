NAME_MAX_LENGTH = 255
INFO_MAX_LENGTH = 2000
TEXT_MAX_LENGTH = 1000

API_VERSION = "v1"

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
