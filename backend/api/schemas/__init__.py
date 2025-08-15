# Схемы для главной страницы
from .homepage import (
    home_page_content_schema,
)

# Схемы для заявок на проект
from .project_request import (
    project_request_create_schema,
)

# Схемы для технологий
from .technologies import (
    technologies_list_schema,
    technology_retrieve_schema,
)

# Схемы для партнеров
from .partners import (
    partners_list_schema,
)

# Схемы для услуг
from .services import (
    services_list_schema,
    service_retrieve_schema,
)

# Схемы для SEO
from .seo import (
    robots_txt_schema,
)

# Схемы для статики
from .sitesettings import (
    site_settings_schema,
)

# Схемы юридических страниц
from .policy import policy_list_schema, policy_retrieve_schema

# flake8: noqa
# ruff: noqa
