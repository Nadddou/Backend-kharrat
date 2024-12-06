import sys
import os

# Path to your Django project
sys.path.insert(0, '/home/kharrax/server')

# Set up the Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'mybackend.settings'

# WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
