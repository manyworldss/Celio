from django.core.management.base import BaseCommand
from django.utils.text import slugify
from travel.models import Country, Attraction, RestaurantPhrase

class Command(BaseCommand):
    help = 'Quick populate travel data for testing'

    def handle(self, *args, **options):
        self.stdout.write('Quick populating travel data...')
        
        # Create comprehensive test countries
        countries_data = [
            {
                'name': 'Italy',
                'code': 'IT',
                'flag_emoji': '🇮🇹',
                'language': 'Italian',
                'language_code': 'it',
                'celiac_awareness': 5,
                'color': '#009246',
                'summary': 'Italy has excellent celiac awareness with widespread gluten-free options and strong legal protections for celiacs.',
                'dining_tips': 'Look for "senza glutine" labels. Many restaurants are certified gluten-free. Italy has some of the best celiac laws in the world.'
            },
            {
                'name': 'France',
                'code': 'FR',
                'flag_emoji': '🇫🇷',
                'language': 'French',
                'language_code': 'fr',
                'celiac_awareness': 4,
                'color': '#0055A4',
                'summary': 'France has good celiac awareness, especially in major cities, with growing gluten-free options.',
                'dining_tips': 'Ask for "sans gluten" options. Many bakeries now offer gluten-free bread. Paris has excellent gluten-free restaurants.'
            },
            {
                'name': 'Spain',
                'code': 'ES',
                'flag_emoji': '🇪🇸',
                'language': 'Spanish',
                'language_code': 'es',
                'celiac_awareness': 4,
                'color': '#AA151B',
                'summary': 'Spain has growing celiac awareness with many gluten-free restaurants and naturally gluten-free traditional dishes.',
                'dining_tips': 'Look for "sin gluten" labels. Spanish cuisine has many naturally gluten-free dishes like paella and tapas.'
            },
            {
                'name': 'Germany',
                'code': 'DE',
                'flag_emoji': '🇩🇪',
                'language': 'German',
                'language_code': 'de',
                'celiac_awareness': 4,
                'color': '#000000',
                'summary': 'Germany has excellent gluten-free product availability and good restaurant awareness.',
                'dining_tips': 'Look for "glutenfrei" products. German supermarkets have extensive gluten-free sections.'
            },
            {
                'name': 'Japan',
                'code': 'JP',
                'flag_emoji': '🇯🇵',
                'language': 'Japanese',
                'language_code': 'ja',
                'celiac_awareness': 2,
                'color': '#BC002D',
                'summary': 'Japan has limited celiac awareness but growing gluten-free options in major cities.',
                'dining_tips': 'Learn key phrases in Japanese. Soy sauce contains gluten - ask for tamari instead.'
            },
            {
                'name': 'United States',
                'code': 'US',
                'flag_emoji': '🇺🇸',
                'language': 'English',
                'language_code': 'en',
                'celiac_awareness': 5,
                'color': '#B22234',
                'summary': 'The United States has excellent celiac awareness with widespread gluten-free options and clear labeling laws.',
                'dining_tips': 'FDA requires clear gluten-free labeling. Most restaurants can accommodate gluten-free requests.'
            }
        ]
        
        for country_data in countries_data:
            country_data['slug'] = slugify(country_data['name'])
            country, created = Country.objects.get_or_create(
                code=country_data['code'],
                defaults=country_data
            )
            if created:
                self.stdout.write(f'Created country: {country.name}')
            else:
                # Update existing country with new data
                for key, value in country_data.items():
                    setattr(country, key, value)
                country.save()
                self.stdout.write(f'Updated country: {country.name}')
                
            # Add attractions for each country
            attractions_data = {
                'IT': [{'name': 'Colosseum', 'local_name': 'Colosseo', 'description': 'Ancient Roman amphitheater and iconic landmark.', 'category': 'monument'}],
                'FR': [{'name': 'Eiffel Tower', 'local_name': 'Tour Eiffel', 'description': 'Iconic iron lattice tower and symbol of Paris.', 'category': 'landmark'}],
                'ES': [{'name': 'Sagrada Familia', 'local_name': 'Sagrada Família', 'description': 'Gaudí\'s masterpiece basilica in Barcelona.', 'category': 'religious'}],
                'DE': [{'name': 'Brandenburg Gate', 'local_name': 'Brandenburger Tor', 'description': 'Historic gate and symbol of Berlin.', 'category': 'monument'}],
                'JP': [{'name': 'Mount Fuji', 'local_name': '富士山', 'description': 'Japan\'s highest mountain and sacred symbol.', 'category': 'landmark'}],
                'US': [{'name': 'Statue of Liberty', 'local_name': 'Statue of Liberty', 'description': 'Symbol of freedom and democracy in New York Harbor.', 'category': 'monument'}]
            }
            
            if country.code in attractions_data:
                for attraction_data in attractions_data[country.code]:
                    attraction_data['gluten_free_info'] = f'Nearby restaurants offer gluten-free options. Check local guides for {country.name}.'
                    Attraction.objects.get_or_create(
                        country=country,
                        name=attraction_data['name'],
                        defaults=attraction_data
                    )
                
            # Add restaurant phrases
            phrases_data = {
                'IT': [
                    {'english': 'I have celiac disease', 'translated': 'Ho la celiachia', 'category': 'general'},
                    {'english': 'Is this gluten-free?', 'translated': 'È senza glutine?', 'category': 'ordering'},
                    {'english': 'I cannot eat wheat', 'translated': 'Non posso mangiare il grano', 'category': 'ingredients'}
                ],
                'FR': [
                    {'english': 'I have celiac disease', 'translated': 'Je suis cœliaque', 'category': 'general'},
                    {'english': 'Is this gluten-free?', 'translated': 'Est-ce sans gluten?', 'category': 'ordering'},
                    {'english': 'I cannot eat wheat', 'translated': 'Je ne peux pas manger de blé', 'category': 'ingredients'}
                ],
                'ES': [
                    {'english': 'I have celiac disease', 'translated': 'Tengo enfermedad celíaca', 'category': 'general'},
                    {'english': 'Is this gluten-free?', 'translated': '¿Esto es sin gluten?', 'category': 'ordering'},
                    {'english': 'I cannot eat wheat', 'translated': 'No puedo comer trigo', 'category': 'ingredients'}
                ],
                'DE': [
                    {'english': 'I have celiac disease', 'translated': 'Ich habe Zöliakie', 'category': 'general'},
                    {'english': 'Is this gluten-free?', 'translated': 'Ist das glutenfrei?', 'category': 'ordering'},
                    {'english': 'I cannot eat wheat', 'translated': 'Ich kann keinen Weizen essen', 'category': 'ingredients'}
                ],
                'JP': [
                    {'english': 'I have celiac disease', 'translated': 'セリアック病です', 'category': 'general'},
                    {'english': 'Is this gluten-free?', 'translated': 'これはグルテンフリーですか？', 'category': 'ordering'},
                    {'english': 'I cannot eat wheat', 'translated': '小麦を食べることができません', 'category': 'ingredients'}
                ],
                'US': [
                    {'english': 'I have celiac disease', 'translated': 'I have celiac disease', 'category': 'general'},
                    {'english': 'Is this gluten-free?', 'translated': 'Is this gluten-free?', 'category': 'ordering'},
                    {'english': 'I cannot eat wheat', 'translated': 'I cannot eat wheat', 'category': 'ingredients'}
                ]
            }
            
            if country.code in phrases_data:
                for phrase_data in phrases_data[country.code]:
                    RestaurantPhrase.objects.get_or_create(
                        country=country,
                        english_text=phrase_data['english'],
                        defaults={
                            'translated_text': phrase_data['translated'],
                            'category': phrase_data['category']
                        }
                    )
        
        # Print summary
        total_countries = Country.objects.count()
        total_attractions = Attraction.objects.count()
        total_phrases = RestaurantPhrase.objects.count()
        
        self.stdout.write(self.style.SUCCESS(f'Successfully populated travel data!'))
        self.stdout.write(f'Total Countries: {total_countries}')
        self.stdout.write(f'Total Attractions: {total_attractions}')
        self.stdout.write(f'Total Phrases: {total_phrases}')