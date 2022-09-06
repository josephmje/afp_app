from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        call_command("makemigrations")
        call_command("migrate")
        # call_command("loaddata", "admin_fixture.json")
        call_command("loaddata", "awardlevel_fixture.json")
        call_command("loaddata", "articletype_fixture.json")
        call_command("loaddata", "examtype_fixture.json")
        call_command("loaddata", "lecturetype_fixture.json")
        call_command("loaddata", "publicationtype_fixture.json")
