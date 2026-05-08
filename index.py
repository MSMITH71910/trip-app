import os
import sys
import shutil
from django.core.wsgi import get_wsgi_application

# Add the project root to the python path
path = os.path.dirname(os.path.dirname(__file__))
if path not in sys.path:
    sys.path.append(path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trip_planner.settings')

def initialize_db():
    if not os.environ.get('DATABASE_URL') and not os.environ.get('POSTGRES_URL'):
        db_path = '/tmp/db.sqlite3'
        template_db = os.path.join(os.path.dirname(__file__), 'db.sqlite3')
        
        # Always check if /tmp/db.sqlite3 exists, if not, copy the template
        if not os.path.exists(db_path):
            print(f"Initializing database at {db_path}...")
            if os.path.exists(template_db):
                try:
                    shutil.copy2(template_db, db_path)
                    # Ensure it's writable
                    os.chmod(db_path, 0o666)
                    print("Database template copied successfully.")
                except Exception as e:
                    print(f"Error copying template database: {e}")
            else:
                print("No template database found in repository.")

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
