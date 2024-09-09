from django.core.management.base import BaseCommand
from  main.models import Run
class Command(BaseCommand):
    help = "To Update the Run Image Num"

    def add_arguments(self, parser):
        parser.add_argument('top', type=int)

    def handle(self, *args, **options):
        #print("command works")
        run = Run.objects.get()
        run.top = options["top"]
        run.save()
        #print("Fin")
