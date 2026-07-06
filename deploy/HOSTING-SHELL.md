# Команды для Shell на хостинге (копировать по одной строке)

## 1. Перейти в проект
```bash
cd ~/www/naslediye34.ru
```

## 2. Узнать, какой Python доступен
```bash
python3 --version
which python3
ls /opt/python/*/bin/python3 2>/dev/null
```

Нужен **Python 3.10 или новее** для Django 5.1.

## 3. Создать venv правильным Python

Если `python3 --version` показывает 3.10+:
```bash
rm -rf venv
python3 -m venv venv
source venv/bin/activate
python --version
```

Если в ISPmanager включили Python 3.10 (путь может отличаться):
```bash
rm -rf venv
/opt/python/3.10/bin/python3 -m venv venv
source venv/bin/activate
python --version
```

## 4. Установить зависимости
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Если снова ошибка «No matching distribution found for Django>=5.1»:
```bash
pip install -r requirements-server.txt
```

## 5. Создать файл .env (это ФАЙЛ, не команда)
```bash
nano .env
```
Вставить содержимое из инструкции, сохранить: Ctrl+O, Enter, Ctrl+X.

## 6. Миграции и статика
```bash
export DJANGO_SETTINGS_MODULE=config.settings.production
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
mkdir -p media
```

## 7. Выйти из venv
```bash
deactivate
```
