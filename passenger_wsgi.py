# -*- coding: utf-8 -*-
"""Точка входа для reg.ru / ISPmanager (формат из официальной инструкции)."""
import os
import sys

sys.path.insert(0, '/var/www/u3569663/data/www/naslediye34.ru')
sys.path.insert(1, '/var/www/u3569663/data/www/naslediye34.ru/venv/lib/python3.11/site-packages')

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings.production'

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
