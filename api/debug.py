"""
Debug endpoint to test what's working on Vercel
"""
import os
import sys
import json

def handler(request):
    """Debug handler to check system info"""
    
    try:
        # Basic system info
        debug_info = {
            'python_version': sys.version,
            'python_path': sys.path[:3],  # First 3 entries
            'working_directory': os.getcwd(),
            'environment_variables': {
                'DJANGO_SECRET_KEY': 'Set' if os.getenv('DJANGO_SECRET_KEY') else 'Not Set',
                'DJANGO_DEBUG': os.getenv('DJANGO_DEBUG', 'Not Set'),
                'DATABASE_URL': 'Set' if os.getenv('DATABASE_URL') else 'Not Set',
                'VERCEL': 'Set' if os.getenv('VERCEL') else 'Not Set',
            }
        }
        
        # Try importing Django
        try:
            import django
            debug_info['django_version'] = django.get_version()
            debug_info['django_import'] = 'SUCCESS'
        except Exception as e:
            debug_info['django_import'] = f'FAILED: {str(e)}'
        
        # Try importing psycopg2
        try:
            import psycopg2
            debug_info['psycopg2_import'] = 'SUCCESS'
        except Exception as e:
            debug_info['psycopg2_import'] = f'FAILED: {str(e)}'
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
            },
            'body': json.dumps(debug_info, indent=2)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
            },
            'body': json.dumps({
                'error': str(e),
                'type': type(e).__name__
            })
        }

# For Vercel
def api(request):
    return handler(request)