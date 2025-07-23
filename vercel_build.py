#!/usr/bin/env python
"""
Vercel build script for Django static files collection
"""
import os
import subprocess
import sys

def main():
    """Collect static files for Vercel deployment"""
    print("🔧 Starting Vercel build process...")
    
    # Set Django settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    
    try:
        # Import Django and setup
        import django
        from django.core.management import execute_from_command_line
        
        print("📦 Setting up Django...")
        django.setup()
        
        print("🗂️  Collecting static files...")
        execute_from_command_line(['manage.py', 'collectstatic', '--noinput', '--clear'])
        
        print("✅ Build completed successfully!")
        
    except Exception as e:
        print(f"❌ Build failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()