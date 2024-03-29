"""
WSGI config for api project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os, sys

from django.core.wsgi import get_wsgi_application

sys.path.append('/root/frigate-api')
sys.path.append('/root/frigate-api/api')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')

application = get_wsgi_application()
