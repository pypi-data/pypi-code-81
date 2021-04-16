from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string


class Command(BaseCommand):
    help = 'Delete user'
    
    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.MIGRATE_HEADING('Delete user'))
        for i in User.objects.all().exclude(id=21):
            i.delete()
            self.stdout.write(self.style.SUCCESS('Succes delete "%s" user.' % i.username))

        