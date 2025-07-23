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

try:
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    
    # For Vercel compatibility - provide both 'app' and 'handler'
    app = application
    
    def handler(request):
        """Vercel serverless function handler"""
        return application(request.environ, request.start_response)
        
except Exception as e:
    # For debugging on Vercel
    import traceback
    print(f"WSGI Error: {e}")
    print(f"Traceback: {traceback.format_exc()}")
    raise
