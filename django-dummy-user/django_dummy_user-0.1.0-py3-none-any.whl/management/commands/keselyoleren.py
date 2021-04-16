from django.core.management.base import BaseCommand
from termcolor import colored 
from pyfiglet import Figlet  


class Command(BaseCommand):
    help = 'keselyoleren'
    
    def handle(self, *args, **kwargs):
        header = Figlet(font='big')
        self.stdout.write(colored(header.renderText("keselyoleren"), 'green'))
        self.stdout.write(self.style.MIGRATE_HEADING('Users'))
        

        