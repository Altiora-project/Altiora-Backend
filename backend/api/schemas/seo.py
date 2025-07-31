from http import HTTPStatus

from drf_spectacular.utils import OpenApiResponse, extend_schema


robots_txt_schema = extend_schema(
    operation_id="robots_txt",
    summary="Получить robots.txt",
    description=(
        "Возвращает содержимое файла robots.txt для поисковых роботов"
    ),
    tags=["SEO"],
    responses={
        HTTPStatus.OK: OpenApiResponse(
            description="robots.txt успешно получен",
        ),
    },
)
