from django.core.management.base import BaseCommand
from django.utils import timezone
class Command(BaseCommand):
    help = 'update the database'
    def handle(self, *args, **kwargs):
        time = timezone.now().strftime('%X')
        self.stdout.write("adding geometries to pozwolenia")