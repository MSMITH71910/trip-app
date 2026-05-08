import os
import sys
import sqlite3
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
        lock_path = '/tmp/db.lock'
        
        # Simple file-based lock to prevent concurrent migrations
        if os.path.exists(lock_path) and (time.time() - os.path.getmtime(lock_path) < 30):
            print("Database is being initialized by another instance, waiting...")
            time.sleep(2)
            return

        try:
            # Create lock
            with open(lock_path, 'w') as f:
                f.write(str(os.getpid()))

            db_exists = os.path.exists(db_path)
            
            # Ensure the file exists
            if not db_exists:
                with open(db_path, 'a'):
                    os.utime(db_path, None)

            # Check if schema is actually there
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='users_user'")
                table_exists = cursor.fetchone()[0] > 0
            except:
                table_exists = False
            conn.close()

            if not table_exists:
                print("Running migrations...")
                call_command('migrate', '--noinput')
                print("Migrations complete.")
            
            # Remove lock
            if os.path.exists(lock_path):
                os.remove(lock_path)
                
        except Exception as e:
            print(f"Database initialization error: {e}")
            if os.path.exists(lock_path):
                os.remove(lock_path)

# Initialize before app starts
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
