from django.core.management.base import BaseCommand, CommandError
import requests

class Command(BaseCommand):
    help = "Import countries from a CSV file."

    def add_arguments(self, parser):
        parser.add_argument(
            '--url',
            type=str,
            default='https://restcountries.com/v3.1/all?fields=name,cca2,cca3,capital,region,subregion,population,area,flags,currencies',
            help='API endpoint URL'
        )
        parser.add_argument(
            '--update',
            action='store_true',
            help='Update existing records'
        )

    def handle(self, *args, **options):
        api_url = options['url']
        
        self.stdout.write(f'Fetching from: {api_url}')

        try:
            response = requests.get(api_url, timeout=30)
            response.raise_for_status()
        except requests.RequestException as e:
            raise CommandError(f'API request failed: {e}')

        data = response.json()
        print(data)

        self.stdout.write(self.style.SUCCESS('Import complete'))