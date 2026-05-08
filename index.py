import os
import sys
import sqlite3
from django.core.wsgi import get_wsgi_application
from django.core.management import call_command

# Add the project root to the python path
path = os.path.dirname(os.path.dirname(__file__))
if path not in sys.path:
    sys.path.append(path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trip_planner.settings')

# Robust /tmp database initialization for Vercel
def initialize_db():
    if not os.environ.get('DATABASE_URL') and not os.environ.get('POSTGRES_URL'):
        db_path = '/tmp/db.sqlite3'
        try:
            # Create a clean file if it doesn't exist
            if not os.path.exists(db_path):
                print(f"Initializing temporary database at {db_path}...")
                # Touch file
                with open(db_path, 'a'):
                    os.utime(db_path, None)
                
                # Run migrations
                call_command('migrate', '--noinput')
        except Exception as e:
            print(f"Database initialization error: {e}")

# Run initialization
initialize_db()

# Disconnect last_login update to prevent writes on login
# This is a critical fix for SQLite on Vercel
try:
    from django.contrib.auth.models import update_last_login
    from django.contrib.auth.signals import user_logged_in
    user_logged_in.disconnect(update_last_login)
except:
    pass

application = get_wsgi_application()
app = application
