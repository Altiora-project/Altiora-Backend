import os
import re
from http import HTTPStatus
from logging import getLogger

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

logger = getLogger(__name__)


class AdminHashMiddleware:
    """
    Middleware для защиты админки по хешу в URL.
    Пример: /admin/<hash>/ активирует сессию, и даёт доступ к /admin/.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.admin_path = "/admin/"
        self.hash_pattern = re.compile(r"^/admin/(?P<hash>[^/]+)/?$")
        self.admin_hash = os.getenv("ADMIN_HASH")

    def __call__(self, request: HttpRequest):
        path = request.path
        logger.info(f"AdminHashMiddleware: входящий путь — {path}")

        # Если пользователь уже авторизован в сессии — пропускаем
        if path.startswith(self.admin_path):
            if request.session.get("admin_authenticated"):
                logger.info("Сессия авторизована — доступ к /admin/ разрешён")
                return self.get_response(request)

            # Если путь содержит хеш, проверяем его
            match = self.hash_pattern.match(path)
            if match:
                provided_hash = match.group("hash")
                if provided_hash == self.admin_hash:
                    logger.info(
                        "Хеш совпадает — авторизуем сессию и перенаправляем"
                    )
                    request.session["admin_authenticated"] = True
                    return redirect(self.admin_path)
                else:
                    logger.warning(f"Неверный хеш в запросе: {provided_hash}")
                    return HttpResponse(status=HTTPStatus.NOT_FOUND)

            # Прямой доступ без хеша и без сессии — запрещён
            logger.warning("Попытка доступа к /admin/ без авторизации и хеша")
            return HttpResponse(status=HTTPStatus.NOT_FOUND)

        # Все остальные пути не трогаем
        return self.get_response(request)
