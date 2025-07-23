from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth.models import User
import os

class Command(BaseCommand):
    help = 'Setup production database with migrations and optional superuser'

    def add_arguments(self, parser):
        parser.add_argument(
            '--create-superuser',
            action='store_true',
            help='Create a superuser account',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Setting up production database...'))
        
        # Run migrations
        self.stdout.write('Running migrations...')
        call_command('migrate', verbosity=1)
        
        # Create superuser if requested
        if options['create_superuser']:
            if not User.objects.filter(is_superuser=True).exists():
                self.stdout.write('Creating superuser...')
                call_command('createsuperuser')
            else:
                self.stdout.write(self.style.WARNING('Superuser already exists.'))
        
        # Collect static files
        self.stdout.write('Collecting static files...')
        call_command('collectstatic', '--noinput', verbosity=1)
        
        self.stdout.write(self.style.SUCCESS('Production setup complete!'))