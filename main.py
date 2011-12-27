import django
import logging
import os

dev = os.environ['SERVER_NAME'] == 'localhost'

os.environ['DJANGO_DEBUG'] = dev and '1' or '0'

if dev:
    logging.info('Development django: %s' % django.__file__)

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi
app = django.core.handlers.wsgi.WSGIHandler()
