from django.core.management.base import BaseCommand, CommandError
import requests
from countries.models import Country
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
        created_count = 0
        updated_count = 0
        skipped_count = 0

        for country in data:
            cca3 = country.get('cca3', '').strip()
            if not cca3 or len(cca3) != 3:
                self.stdout.write(self.style.WARNING(f'Skipping country with invalid cca3: "{cca3}"'))
                skipped_count += 1
                continue

            cca2 = country.get('cca2', '').strip()
            if not cca2 or len(cca2) != 2:
                self.stdout.write(self.style.WARNING(f'Skipping country {cca3} with invalid cca2: "{cca2}"'))
                skipped_count += 1
                continue

            name_data = country.get('name', {})
            capitals = country.get('capital') or []
            flags = country.get('flags', {})

            # Validate URL
            flag_url = flags.get('png', '').strip()
            if flag_url and not flag_url.startswith('http'):
                flag_url = ''

            # Validate numeric fields
            population = country.get('population')
            population = int(population) if population is not None else None

            area = country.get('area')
            area = float(area) if area is not None else None

            defaults = {
                'common_name': name_data.get('common', '').strip()[:255],
                'official_name': name_data.get('official', '').strip()[:255],
                'native_name': name_data.get('nativeName'),
                'cca2': cca2,
                'capital': capitals[0].strip()[:255] if capitals else None,
                'region': country.get('region', '').strip()[:255] or None,
                'subregion': country.get('subregion', '').strip()[:255] or None,
                'population': population,
                'area': area,
                'flag_url': flag_url,
                'currencies': country.get('currencies'),
            }

            obj, created = Country.objects.update_or_create(
                cca3=cca3,
                defaults=defaults,
            )

            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'Created: {obj}'))
            else:
                updated_count += 1
                self.stdout.write(f'Updated: {obj}')

        self.stdout.write(self.style.SUCCESS(
            f'\nImport complete: {created_count} created, '
            f'{updated_count} updated, {skipped_count} skipped'
        ))