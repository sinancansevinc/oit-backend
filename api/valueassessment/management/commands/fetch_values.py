from django.core.management.base import BaseCommand
from valueassessment import tasks


class Command(BaseCommand):
    help = "Fetch doctor commercial status from metabase. Also create new doctors."

    def handle(self, *args, **options):
        tasks.assign_value_assessments()
