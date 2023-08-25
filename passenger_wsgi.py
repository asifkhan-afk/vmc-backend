import sys
import os

# Add the project directory to the sys.path
sys.path.append('/home/a2zcyber/vmc.a2zcyberpark.com/vmc')

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ['DJANGO_SETTINGS_MODULE'] = 'vmc.settings'

# Import the Django application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
