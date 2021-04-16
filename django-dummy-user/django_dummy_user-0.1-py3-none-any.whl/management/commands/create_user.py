from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from faker import Faker
import dummy


class Command(BaseCommand):
    help = 'Displays current time'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help="total jumblah users")

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        self.stdout.write(self.style.MIGRATE_HEADING('Create random user'))
        for i in range(total):
            user = User.objects.create_user(username=dummy.username(), email=dummy.email(), password="password")
            self.stdout.write(self.style.MIGRATE_LABEL('User "%s" successfully added' % user.username)) 
            self.stdout.write(self.style.SUCCESS("OK"))
        