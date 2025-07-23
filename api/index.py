"""
Minimal Vercel serverless function to test if Python is working
"""
import os
import json

def handler(request):
    """Simple test handler that doesn't require Django"""
    
    # Check environment variables
    env_vars = {
        'DJANGO_SECRET_KEY': 'Set' if os.getenv('DJANGO_SECRET_KEY') else 'Not Set',
        'DJANGO_DEBUG': os.getenv('DJANGO_DEBUG', 'Not Set'),
        'DATABASE_URL': 'Set' if os.getenv('DATABASE_URL') else 'Not Set',
        'VERCEL': 'Set' if os.getenv('VERCEL') else 'Not Set',
    }
    
    response_data = {
        'message': 'Python is working on Vercel!',
        'status': 'OK',
        'environment_variables': env_vars
    }
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
        },
        'body': json.dumps(response_data)
    }

# For Vercel
def api(request):
    return handler(request)