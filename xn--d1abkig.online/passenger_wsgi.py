# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, '/var/www/u2179681/data/www/xn--d1abkig.online/supermediconline')
sys.path.insert(1, '/var/www/u2179681/data/djangoenv/lib/python3.10/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'supermediconline.settings'
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()