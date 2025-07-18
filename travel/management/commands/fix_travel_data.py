from django.core.management.base import BaseCommand
from django.db import transaction
from travel.models import Country, RestaurantPhrase, Attraction

class Command(BaseCommand):
    help = 'Fix and populate travel data'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write('Fixing travel data...')
        
        # Create basic countries if they don't exist
        countries_data = [
            {
                'name': 'Italy',
                'code': 'IT',
                'flag_emoji': '🇮🇹',
                'language': 'Italian',
                'language_code': 'it',
                'celiac_awareness': 5,
                'summary': 'Italy has excellent celiac awareness with many gluten-free options.',
                'dining_tips': 'Look for "senza glutine" on menus and ask for gluten-free options.',
            },
            {
                'name': 'France',
                'code': 'FR',
                'flag_emoji': '🇫🇷',
                'language': 'French',
                'language_code': 'fr',
                'celiac_awareness': 4,
                'summary': 'France has good celiac awareness, especially in major cities.',
                'dining_tips': 'Ask for "sans gluten" options and check with restaurants.',
            },
            {
                'name': 'United States',
                'code': 'US',
                'flag_emoji': '🇺🇸',
                'language': 'English',
                'language_code': 'en',
                'celiac_awareness': 4,
                'summary': 'The US has excellent gluten-free awareness and options.',
                'dining_tips': 'Many restaurants offer gluten-free menus. Always inform staff of celiac disease.',
            },
        ]
        
        for country_data in countries_data:
            country, created = Country.objects.get_or_create(
                code=country_data['code'],
                defaults=country_data
            )
            if created:
                self.stdout.write(f'Created country: {country.name}')
            
            # Add sample attractions
            if country.code == 'IT':
                attractions_data = [
                    {
                        'name': 'Colosseum',
                        'local_name': 'Colosseo',
                        'description': 'Ancient Roman amphitheater and iconic symbol of Imperial Rome.',
                        'category': 'monument',
                    },
                    {
                        'name': 'Vatican Museums',
                        'local_name': 'Musei Vaticani',
                        'description': 'World-renowned art collection including the Sistine Chapel.',
                        'category': 'museum',
                    },
                ]
                
                for attraction_data in attractions_data:
                    attraction, created = Attraction.objects.get_or_create(
                        country=country,
                        name=attraction_data['name'],
                        defaults=attraction_data
                    )
                    if created:
                        self.stdout.write(f'Created attraction: {attraction.name}')
            
            # Add sample phrases
            phrases_data = [
                {
                    'category': 'general',
                    'english_text': 'I have celiac disease. I cannot eat gluten.',
                    'translated_text': {
                        'IT': 'Ho la celiachia. Non posso mangiare glutine.',
                        'FR': 'Je suis atteint(e) de la maladie cœliaque. Je ne peux pas manger de gluten.',
                        'US': 'I have celiac disease. I cannot eat gluten.',
                    }.get(country.code, 'I have celiac disease. I cannot eat gluten.'),
                    'pronunciation': '',
                },
                {
                    'category': 'ordering',
                    'english_text': 'Do you have gluten-free options?',
                    'translated_text': {
                        'IT': 'Avete opzioni senza glutine?',
                        'FR': 'Avez-vous des options sans gluten?',
                        'US': 'Do you have gluten-free options?',
                    }.get(country.code, 'Do you have gluten-free options?'),
                    'pronunciation': '',
                },
            ]
            
            for phrase_data in phrases_data:
                phrase, created = RestaurantPhrase.objects.get_or_create(
                    country=country,
                    english_text=phrase_data['english_text'],
                    defaults=phrase_data
                )
                if created:
                    self.stdout.write(f'Created phrase: {phrase.english_text[:30]}...')
        
        self.stdout.write(self.style.SUCCESS('Successfully fixed travel data!'))