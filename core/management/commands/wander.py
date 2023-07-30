from django.core.management.base import BaseCommand

from core.services.wikibot import wander


class Command(BaseCommand):
    help = "My shiny new management command."

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        wander()
