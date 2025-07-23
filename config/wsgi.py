"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.
Also provides 'app' and 'handler' for Vercel compatibility.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
import sys

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Initialize Django application
from django.core.wsgi import get_wsgi_application

# Create the WSGI application
application = get_wsgi_application()

# For Vercel compatibility - provide 'app' variable
app = application

# For Vercel compatibility - provide 'handler' function  
def handler(environ, start_response):
    """Vercel serverless function handler"""
    return application(environ, start_response)
