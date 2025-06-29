from django.core.management.base import BaseCommand
from travel.models import Country, DishesToAvoid, RestaurantPhrase

class Command(BaseCommand):
    help = 'Populate the database with sample travel guide countries'

    def handle(self, *args, **options):
        # Clear existing data
        Country.objects.all().delete()
        
        # Sample countries data
        countries_data = [
            {
                'name': 'Japan',
                'code': 'JP',
                'flag_emoji': '🇯🇵',
                'language': 'Japanese',
                'language_code': 'ja',
                'celiac_awareness': 2,
                'summary': 'Japan has limited celiac awareness, but gluten-free options are growing in major cities. Rice-based dishes are naturally safe.',
                'dining_tips': 'Look for rice-based dishes, avoid soy sauce (contains wheat), and learn key phrases in Japanese.'
            },
            {
                'name': 'Italy',
                'code': 'IT',
                'flag_emoji': '🇮🇹',
                'language': 'Italian',
                'language_code': 'it',
                'celiac_awareness': 5,
                'summary': 'Italy has excellent celiac awareness with many certified gluten-free restaurants and products widely available.',
                'dining_tips': 'Look for "senza glutine" labels, many restaurants offer gluten-free pasta, and pharmacies sell gluten-free products.'
            },
            {
                'name': 'France',
                'code': 'FR',
                'flag_emoji': '🇫🇷',
                'language': 'French',
                'language_code': 'fr',
                'celiac_awareness': 4,
                'summary': 'France has good celiac awareness, especially in Paris. Many bakeries now offer gluten-free options.',
                'dining_tips': 'Ask for "sans gluten" options, avoid traditional bread and pastries, focus on meat and vegetable dishes.'
            },
            {
                'name': 'Thailand',
                'code': 'TH',
                'flag_emoji': '🇹🇭',
                'language': 'Thai',
                'language_code': 'th',
                'celiac_awareness': 2,
                'summary': 'Thailand has low celiac awareness, but rice-based cuisine offers many naturally gluten-free options.',
                'dining_tips': 'Stick to rice dishes, avoid soy sauce and fish sauce, communicate dietary needs clearly with restaurant staff.'
            },
            {
                'name': 'Germany',
                'code': 'DE',
                'flag_emoji': '🇩🇪',
                'language': 'German',
                'language_code': 'de',
                'celiac_awareness': 4,
                'summary': 'Germany has good celiac awareness with many gluten-free products available in supermarkets and restaurants.',
                'dining_tips': 'Look for "glutenfrei" labels, many supermarkets have dedicated gluten-free sections, and beer alternatives are available.'
            },
            {
                'name': 'Spain',
                'code': 'ES',
                'flag_emoji': '🇪🇸',
                'language': 'Spanish',
                'language_code': 'es',
                'celiac_awareness': 4,
                'summary': 'Spain has good celiac awareness with a strong celiac association and many certified restaurants.',
                'dining_tips': 'Look for "sin gluten" options, many restaurants are celiac-certified, and gluten-free products are widely available.'
            },
            {
                'name': 'United States',
                'code': 'US',
                'flag_emoji': '🇺🇸',
                'language': 'English',
                'language_code': 'en',
                'celiac_awareness': 5,
                'summary': 'The US has excellent celiac awareness with widespread gluten-free options in restaurants and grocery stores.',
                'dining_tips': 'Most restaurants offer gluten-free menus, grocery stores have dedicated sections, and labeling laws are strict.'
            },
            {
                'name': 'India',
                'code': 'IN',
                'flag_emoji': '🇮🇳',
                'language': 'Hindi',
                'language_code': 'hi',
                'celiac_awareness': 2,
                'summary': 'India has limited celiac awareness, but rice-based dishes and traditional cuisine offer many naturally gluten-free options.',
                'dining_tips': 'Focus on rice dishes, lentil-based foods, and traditional curries. Avoid wheat-based breads and noodles.'
            }
        ]
        
        # Create countries
        for country_data in countries_data:
            country = Country.objects.create(**country_data)
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created country: {country.name}')
            )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully populated {len(countries_data)} countries!')
        )