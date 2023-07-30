from django.conf import settings
from django.core.management.base import BaseCommand

from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = "Creates the super user account if it does not exist"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        email = settings.ADMIN_EMAIL
        password = settings.ADMIN_PASSWORD

        if User.objects.filter(email=email).exists():
            self.stdout.write("The super user account already exists")
            return

        User.objects.create_superuser(email=email, password=password)

        self.stdout.write("The super user account has been created")
