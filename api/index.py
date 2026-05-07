import os
import sys
from django.core.wsgi import get_wsgi_application
from django.core.management import call_command

# Add the project root to the python path
path = os.path.dirname(os.path.dirname(__file__))
if path not in sys.path:
    sys.path.append(path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trip_planner.settings')

# Auto-run migrations on Vercel if using the /tmp workaround
if not os.environ.get('DATABASE_URL') and not os.environ.get('POSTGRES_URL'):
    db_path = '/tmp/db.sqlite3'
    if not os.path.exists(db_path):
        print("Initializing temporary database...")
        try:
            call_command('migrate', '--noinput')
        except Exception as e:
            print(f"Migration error: {e}")

application = get_wsgi_application()
app = application
