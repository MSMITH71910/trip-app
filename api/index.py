"""
Minimal Vercel serverless function to test if Python is working
"""

def handler(request):
    """Simple test handler that doesn't require Django"""
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
        },
        'body': '{"message": "Python is working on Vercel!", "status": "OK"}'
    }

# For Vercel
def api(request):
    return handler(request)