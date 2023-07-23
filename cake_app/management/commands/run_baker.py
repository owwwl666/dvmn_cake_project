from django.core.management.base import BaseCommand
from cake_app.bakerbot import run_baker


class Command(BaseCommand):
    help = 'run baker bot'

    def handle(self, *args, **options):
        run_baker()
