import os
import sys
import time
from django.core.wsgi import get_wsgi_application
from django.core.management import call_command

# Add the project root to the python path
path = os.path.dirname(os.path.dirname(__file__))
if path not in sys.path:
    sys.path.append(path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trip_planner.settings')

def initialize_db():
    if not os.environ.get('DATABASE_URL') and not os.environ.get('POSTGRES_URL'):
        db_path = '/tmp/db.sqlite3'
        
        # If it doesn't exist, migrate with retries
        if not os.path.exists(db_path):
            print("Initializing database...")
            for i in range(3):
                try:
                    call_command('migrate', '--noinput')
                    print("Migration successful.")
                    break
                except Exception as e:
                    print(f"Migration attempt {i+1} failed: {e}")
                    time.sleep(1)

# Run initialization
initialize_db()

# Prevent writes on login
try:
    from django.contrib.auth.models import update_last_login
    from django.contrib.auth.signals import user_logged_in
    user_logged_in.disconnect(update_last_login)
except:
    pass

application = get_wsgi_application()
app = application
