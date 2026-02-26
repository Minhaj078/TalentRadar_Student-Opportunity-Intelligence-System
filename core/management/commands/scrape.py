from django.core.management.base import BaseCommand
from core.utils import real_scraper

class Command(BaseCommand):
    help = "Run real scraper to fetch opportunities"

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting scraper...")
        real_scraper()
        self.stdout.write(self.style.SUCCESS("Scraping completed successfully!"))