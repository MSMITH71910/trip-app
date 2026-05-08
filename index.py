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
    try:
        if not os.environ.get('DATABASE_URL') and not os.environ.get('POSTGRES_URL'):
            db_path = '/tmp/db.sqlite3'
            template_db = os.path.join(os.path.dirname(__file__), 'db.sqlite3')
            
            if not os.path.exists(db_path):
                if os.path.exists(template_db):
                    shutil.copy2(template_db, db_path)
                    os.chmod(db_path, 0o666)
                else:
                    # Fallback: create empty file
                    with open(db_path, 'w') as f:
                        pass
                    from django.core.management import call_command
                    call_command('migrate', '--noinput')
    except Exception as e:
        print(f"DB Init Error: {e}")

# Run initialization
initialize_db()

# Prevent writes on login (critical for serverless SQLite)
try:
    from django.contrib.auth.models import update_last_login
    from django.contrib.auth.signals import user_logged_in
    user_logged_in.disconnect(update_last_login)
except:
    pass

application = get_wsgi_application()
app = application
