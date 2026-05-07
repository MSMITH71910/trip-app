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
    # Only run this if we are NOT using a real database
    if not os.environ.get('DATABASE_URL') and not os.environ.get('POSTGRES_URL'):
        db_path = '/tmp/db.sqlite3'
        
        # Ensure the file is writable by creating/touching it
        try:
            print(f"Checking/Initializing database at {db_path}...")
            # Try to open/create the file to ensure it's writable
            with open(db_path, 'a'):
                os.utime(db_path, None)
            
            # Use a lock-like check to avoid multiple simultaneous migrations if possible
            # But in Lambda usually one init per instance
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Check if migrations have already run by looking for a core table
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users_user';")
            if not cursor.fetchone():
                print("Running migrations on temporary database...")
                conn.close() # Close before running migrate
                call_command('migrate', '--noinput')
            else:
                print("Database tables already exist.")
                conn.close()
        except Exception as e:
            print(f"Database initialization error: {e}")

# Run initialization before getting the application
initialize_db()

application = get_wsgi_application()
app = application
