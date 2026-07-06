# Деплой Django на reg.ru (ISPmanager)

Пошаговая инструкция по опыту проекта «Наследие». Подходит для других Django-сайтов на том же хостинге.

**Хостинг:** reg.ru, панель ISPmanager, сервер `server240.hosting.reg.ru`  
**Тариф:** виртуальный хостинг с Python (ispmanager)

---

## Содержание

1. [Что нужно знать заранее](#1-что-нужно-знать-заранее)
2. [Подготовка проекта локально](#2-подготовка-проекта-локально)
3. [Настройка в ISPmanager](#3-настройка-в-ispmanager)
4. [База данных MySQL](#4-база-данных-mysql)
5. [Загрузка файлов на сервер](#5-загрузка-файлов-на-сервер)
6. [Команды в Shell (полный блок)](#6-команды-в-shell-полный-блок)
7. [passenger_wsgi.py](#7-passenger_wsgipy)
8. [Файл .env](#8-файл-env)
9. [Статика, CSS, медиа](#9-статика-css-медиа)
10. [Favicon](#10-favicon)
11. [Перезапуск и проверка](#11-перезапуск-и-проверка)
12. [Типичные ошибки](#12-типичные-ошибки)
13. [Чеклист перед открытием сайта](#13-чеклист-перед-открытием-сайта)
14. [Шаблон для нового сайта](#14-шаблон-для-нового-сайта)

---

## 1. Что нужно знать заранее

### Версии Python на сервере

| Команда | Результат | Использовать? |
|---------|-----------|---------------|
| `python --version` | **3.6.8** | ❌ Нет |
| `python3 --version` | **3.8.6** | ❌ Нет (для Django 5.x) |
| `python3.11` | команда не найдена | ❌ Нет |
| `/opt/python/python-3.11/bin/python3` | **3.11.x** | ✅ Да |
| `/opt/python/python-3.10.1/bin/python3` | **3.10.x** | ✅ Да |

Список всех версий:

```bash
ls /opt/python/*/bin/python3
```

**Правило:** venv создавать **только** полным путём:

```bash
/opt/python/python-3.11/bin/python3 -m venv venv
```

Не `/opt/python/3.11/` — такого пути нет. Правильный формат: `/opt/python/python-3.11/bin/python3`.

### Django и Python

| Django | Минимальный Python |
|--------|-------------------|
| 5.1+ | 3.10+ |
| 4.2 LTS | 3.8+ |

Для Django 5.x на reg.ru используйте **Python 3.10 или 3.11**.

### Пути на сервере (подставьте свои)

| Параметр | Пример «Наследие» |
|----------|-------------------|
| Логин хостинга | `u3569663` |
| Домен | `naslediye34.ru` |
| Корень сайта | `/var/www/u3569663/data/www/naslediye34.ru` |
| В Shell | `~/www/naslediye34.ru` |
| Логи | `~/logs/naslediye34.ru.error.log` |

Формула пути:

```
/var/www/<ЛОГИН>/data/www/<ДОМЕН>/
```

### reg.ru: Python в панели

**Обязательно включить оба пункта** (иначе Python сбрасывается после сохранения):

- ✅ **CGI-скрипты**
- ✅ **Python** → версия `python-3.11`

Файл `passenger_wsgi.py` должен **уже лежать в корне сайта** до включения Python в панели.

**Не используйте** `.htaccess` с директивами Passenger на reg.ru — панель настраивает это сама, лишний `.htaccess` мешает.

Перезапуск приложения на reg.ru:

```bash
touch .restart-app
```

Не `tmp/restart.txt` — на reg.ru используется `.restart-app`.

---

## 2. Подготовка проекта локально

### Структура settings (рекомендуется)

```
config/settings/
  base.py          # общие настройки + чтение .env
  development.py   # локальная разработка
  production.py    # продакшен
```

### requirements.txt (минимум для MySQL на reg.ru)

```txt
Django>=5.1,<5.2
django-environ>=0.11.2
PyMySQL>=1.1.1
cryptography>=42.0.0
Pillow>=10.4.0
whitenoise>=6.7.0
```

**Важно:** `cryptography` обязателен — без него MySQL выдаёт:

```
RuntimeError: 'cryptography' package is required for caching_sha2_password
```

### PyMySQL в config/__init__.py

```python
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass
```

### production.py — настройки для shared-хостинга

```python
DEBUG = False

CSRF_TRUSTED_ORIGINS = ['https://ваш-домен.ru', 'https://www.ваш-домен.ru']
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Без многопоточного сжатия — иначе collectstatic падает с "can't start new thread"
STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.StaticFilesStorage',
    },
}
```

### Собрать CSS до загрузки (если Tailwind)

```bash
npm install
npm run build:css
```

Папка `static/dist/` должна попасть на сервер (она в `.gitignore`).

### Что НЕ загружать на сервер

- `.env` — создать на сервере вручную (секреты)
- `venv/` — создать на сервере
- `staticfiles/` — собрать на сервере через `collectstatic`
- `db.sqlite3`, `__pycache__/`, `.git/`

---

## 3. Настройка в ISPmanager

### Создать сайт

1. **Сайты** → домен (например `example.ru`)
2. Псевдоним: `www.example.ru`
3. **SSL** — включить, выбрать сертификат Let's Encrypt
4. **Перенаправлять HTTP → HTTPS** — рекомендуется включить

### Включить Python

**Сайты** → домен → **Изменить** → **Дополнительные возможности**:

| Пункт | Значение |
|-------|----------|
| CGI-скрипты | ✅ |
| Python | ✅ |
| Версия Python | `python-3.11` (та же, что для venv) |
| PHP | можно выключить |

**Сохранить.** Если Python сбрасывается — сначала сохраните только CGI, затем снова включите Python.

### Индексная страница

Поле «Индексная страница» (`index.php index.html`) для Django не критично, если работает Passenger. Если в корне лежат пустые `index.html` / `index.php` — **удалите их**.

---

## 4. База данных MySQL

### В ISPmanager

1. **Базы данных** → MySQL → создать БД и пользователя
2. Записать: имя БД, пользователь, пароль
3. Хост почти всегда: `localhost`, порт: `3306`

### В phpMyAdmin

Имя БД видно в списке слева (например `u3569663_localhost`). Таблицы создаёт `migrate` — вручную ничего не создавать.

### DATABASES в settings

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST', default='localhost'),
        'PORT': env('DB_PORT', default='3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
```

---

## 5. Загрузка файлов на сервер

Способы: FTP/SFTP, файловый менеджер ISPmanager, `git clone` в Shell.

Целевая папка:

```bash
~/www/ВАШ-ДОМЕН.ru/
```

В корне должны быть: `manage.py`, `config/`, `apps/`, `templates/`, `static/`, `requirements.txt`.

---

## 6. Команды в Shell (полный блок)

Подставьте свой путь к Python и домен. Выполняйте **после** загрузки файлов.

```bash
# === НАСТРОЙКИ (изменить под новый сайт) ===
DOMAIN="naslediye34.ru"
PYTHON="/opt/python/python-3.11/bin/python3"
SITE_ROOT="$HOME/www/$DOMAIN"

cd "$SITE_ROOT"

# 1. Виртуальное окружение
rm -rf venv
$PYTHON -m venv venv
source venv/bin/activate
python --version   # должно быть 3.10+

# 2. Зависимости
pip install --upgrade pip
pip install -r requirements.txt

# 3. Проверка .env (создать вручную, если нет — см. раздел 8)
test -f .env && echo "OK: .env есть" || echo "Создайте .env: nano .env"

# 4. Миграции и статика
export DJANGO_SETTINGS_MODULE=config.settings.production
python manage.py migrate
python manage.py collectstatic --noinput
mkdir -p media
chmod 755 media

# 5. Проверка passenger_wsgi (см. раздел 7)
python -c "import passenger_wsgi; print('passenger_wsgi OK')"

# 6. Администратор (интерактивно)
python manage.py createsuperuser
```

---

## 7. passenger_wsgi.py

Файл в **корне сайта** (рядом с `manage.py`). Формат **reg.ru** (официальная инструкция):

```python
# -*- coding: utf-8 -*-
import os, sys

sys.path.insert(0, '/var/www/u3569663/data/www/naslediye34.ru')
sys.path.insert(1, '/var/www/u3569663/data/www/naslediye34.ru/venv/lib/python3.11/site-packages')

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings.production'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### Что менять для нового сайта

| Строка | Заменить |
|--------|----------|
| `sys.path.insert(0, ...)` | полный путь к корню проекта |
| `sys.path.insert(1, ...)` | путь к `venv/lib/python3.11/site-packages` |
| `DJANGO_SETTINGS_MODULE` | модуль настроек, например `config.settings.production` |

Версия в пути `python3.11` должна совпадать с версией venv (`ls venv/lib/`).

### Создать одной командой в Shell

```bash
cd ~/www/ВАШ-ДОМЕН.ru

cat > passenger_wsgi.py << 'EOF'
# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, '/var/www/u3569663/data/www/naslediye34.ru')
sys.path.insert(1, '/var/www/u3569663/data/www/naslediye34.ru/venv/lib/python3.11/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings.production'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
EOF
```

(замените пути перед выполнением)

---

## 8. Файл .env

Создать **на сервере**, не коммитить в git:

```bash
nano ~/www/ВАШ-ДОМЕН.ru/.env
```

### Шаблон

```env
DJANGO_SETTINGS_MODULE=config.settings.production
DJANGO_SECRET_KEY=сгенерируйте-длинную-случайную-строку
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=example.ru,www.example.ru
DJANGO_CSRF_TRUSTED_ORIGINS=https://example.ru,https://www.example.ru

USE_SQLITE=False
DB_NAME=u123456_dbname
DB_USER=u123456_user
DB_PASSWORD=ваш_пароль
DB_HOST=localhost
DB_PORT=3306

SITE_URL=https://example.ru
SITE_NAME=Название сайта
```

### Сгенерировать SECRET_KEY

```bash
source venv/bin/activate
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## 9. Статика, CSS, медиа

### Статика (CSS, JS, картинки из static/)

```bash
export DJANGO_SETTINGS_MODULE=config.settings.production
python manage.py collectstatic --noinput
```

Результат: папка `staticfiles/`. WhiteNoise раздаёт `/static/` через Django.

### CSS (Tailwind)

Локально:

```bash
npm run build:css
```

Загрузить `static/dist/` на сервер → снова `collectstatic`.

### Медиа (загрузки из админки)

Папка `media/` в корне проекта. Для раздачи через Nginx (опционально) в ISPmanager → доп. директивы Nginx:

```nginx
location /media/ {
    alias /var/www/u3569663/data/www/naslediye34.ru/media/;
}
```

---

## 10. Favicon

1. Положить файл: `static/images/favicon.ico` (или `.png`)
2. В `templates/base.html` в `<head>`:

```html
{% load static %}
<link rel="icon" href="{% static 'images/favicon.ico' %}" sizes="32x32">
```

3. На сервере: `collectstatic` + `touch .restart-app`
4. В браузере: Ctrl+F5 (favicon кэшируется)

---

## 11. Перезапуск и проверка

### Перезапуск Django (reg.ru)

```bash
cd ~/www/ВАШ-ДОМЕН.ru
touch .restart-app
```

### Проверка настроек

```bash
source venv/bin/activate
export DJANGO_SETTINGS_MODULE=config.settings.production
python manage.py check --deploy
```

2 предупреждения про HSTS и SSL redirect — не критично, если редирект на HTTPS включён в панели.

### Логи ошибок

```bash
tail -30 ~/logs/ВАШ-ДОМЕН.ru.error.log
```

### Браузер

- `https://ваш-домен.ru`
- `https://ваш-домен.ru/admin/`

---

## 12. Типичные ошибки

### `No matching distribution found for Django>=5.1`

**Причина:** venv создан от старого Python (3.8).  
**Решение:** пересоздать venv через `/opt/python/python-3.11/bin/python3`.

### `cryptography package is required`

**Решение:** `pip install cryptography` (добавить в requirements.txt).

### `can't start new thread` при collectstatic

**Причина:** WhiteNoise `CompressedManifestStaticFilesStorage` на shared-хостинге.  
**Решение:** в `production.py` использовать `whitenoise.storage.StaticFilesStorage`.

### `directory index ... is forbidden`

**Причина:** Python/CGI не включены в панели, Passenger не запускается.  
**Решение:** включить CGI + Python, проверить `passenger_wsgi.py`, удалить `.htaccess` и пустые `index.html`.

### Python в панели сбрасывается после сохранения

**Решение:** включить **CGI-скрипты** вместе с Python; `passenger_wsgi.py` должен быть в корне до сохранения.

### `python3.11: команда не найдена`

**Решение:** использовать полный путь `/opt/python/python-3.11/bin/python3`.

### Сайт без стилей

**Решение:** `npm run build:css` локально → загрузить `static/dist/` → `collectstatic`.

### Странные ошибки в Shell (`{.{env...`, `.env: команда не найдена`)

**Причина:** в терминал попал мусор от автодополнения.  
**Решение:** вводить команды по одной строке. `.env` — это файл (`nano .env`), не команда.

---

## 13. Чеклист перед открытием сайта

- [ ] Файлы загружены в `~/www/ДОМЕН/`
- [ ] venv на Python 3.10+ (`/opt/python/python-3.11/bin/python3`)
- [ ] `pip install -r requirements.txt` без ошибок
- [ ] `.env` создан на сервере, `DEBUG=False`
- [ ] `ALLOWED_HOSTS` и `CSRF_TRUSTED_ORIGINS` с доменом
- [ ] `python manage.py migrate`
- [ ] `python manage.py collectstatic --noinput`
- [ ] `passenger_wsgi.py` с правильными путями
- [ ] В панели: **CGI + Python 3.11** включены
- [ ] SSL включён
- [ ] `createsuperuser` для админки
- [ ] `static/dist/` загружен (если Tailwind)
- [ ] `touch .restart-app`
- [ ] Сайт открывается в браузере

---

## 14. Шаблон для нового сайта

Скопируйте и заполните перед деплоем:

```
Логин хостинга:     u________
Домен:              ________________.ru
Путь к сайту:       /var/www/u________/data/www/________________.ru
Python для venv:    /opt/python/python-3.11/bin/python3
Версия venv:        python3.11  (проверить: ls venv/lib/)

MySQL:
  DB_NAME:          u_________
  DB_USER:          u_________
  DB_PASSWORD:      ********
  DB_HOST:          localhost

DJANGO_SETTINGS_MODULE: config.settings.production
```

### Порядок действий (кратко)

```
1. Локально: npm run build:css (если нужно)
2. ISPmanager: сайт + SSL + БД MySQL
3. Загрузить файлы на сервер
4. Shell: venv → pip install → .env → migrate → collectstatic
5. Создать passenger_wsgi.py (пути!)
6. ISPmanager: CGI + Python 3.11 → Сохранить
7. createsuperuser
8. touch .restart-app
9. Открыть сайт в браузере
```

---

## Полезные ссылки

- [reg.ru: Как установить Django](https://help.reg.ru/support/hosting/php-asp-net-i-skripty/kak-ustanovit-django-na-hosting)
- [ispmanager: Установка Django](https://www.ispmanager.ru/docs/ispmanager/ustanovka-django)

---

*Документ создан по опыту деплоя naslediye34.ru, июль 2026.*
