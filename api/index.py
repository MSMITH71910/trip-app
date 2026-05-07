import os
import sys
from django.core.wsgi import get_wsgi_application

# Add the project root to the python path
path = os.path.dirname(os.path.dirname(__file__))
if path not in sys.path:
    sys.path.append(path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trip_planner.settings')

application = get_wsgi_application()
app = application
