import os
import sys

# Add the project root to the python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from trip_planner.wsgi import application

# This variable name is important for Vercel
app = application
