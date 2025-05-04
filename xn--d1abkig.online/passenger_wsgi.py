#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

# 1) Путь к корню вашего Django-проекта (там, где лежат папки supermedicapp и суперпакет supermediconline)
BASE_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.join(BASE_DIR, 'supermediconline')

# 2) Добавляем в PYTHONPATH
sys.path.insert(0, PROJECT_ROOT)

# 3) Указываем Django-настройки
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'supermediconline.settings')

# 4) Запускаем WSGI-приложение
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
