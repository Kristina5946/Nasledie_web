#!/bin/bash
# Запускать на сервере в каталоге проекта (где manage.py)
set -e

cd "$(dirname "$0")/.."

echo "==> Виртуальное окружение"
python3 -m venv venv
source venv/bin/activate

echo "==> Зависимости Python"
pip install --upgrade pip
pip install -r requirements.txt

echo "==> CSS (если установлен Node.js)"
if command -v npm >/dev/null 2>&1; then
  npm install
  npm run build:css
else
  echo "npm не найден — соберите CSS локально и загрузите static/dist/ на сервер"
fi

echo "==> Проверка настроек"
python manage.py check --deploy

echo "==> Миграции"
python manage.py migrate

echo "==> Создание администратора (введите логин, email, пароль)"
python manage.py createsuperuser

echo "==> Статика"
python manage.py collectstatic --noinput

echo "==> Каталог media"
mkdir -p media
chmod 755 media

echo "Готово."
