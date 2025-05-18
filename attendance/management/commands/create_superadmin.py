from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    help = 'Creates superadmin user if it does not exist'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        username = os.getenv('DJANGO_SUPERUSER_USERNAME', 'admin')
        email = os.getenv('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
        password = os.getenv('DJANGO_SUPERUSER_PASSWORD', 'adminpass')

        if User.objects.filter(username=username).exists():
            self.stdout.write(f'Superuser {username} already exists.')
        else:
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(f'Superuser {username} created.')
