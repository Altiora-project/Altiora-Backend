#!/bin/bash
set -e

echo "Запускаем Celery worker..."
exec "$@"
