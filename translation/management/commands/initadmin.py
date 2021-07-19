from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os


class Command(BaseCommand):
    def handle(self, *args, **options):
        if User.objects.count() == 0:
            username = os.environ.get('SUPERUSER_USERNAME')
            password = os.environ.get('SUPERUSER_PASSWORD')
            admin = User.objects.create_superuser(username=username, password=password)
            admin.is_active = True
            admin.save()
        else:
            print('Admin accounts can only be initialized if no Accounts exist')
