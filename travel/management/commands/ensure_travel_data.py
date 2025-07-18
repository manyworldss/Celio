from django.core.management.base import BaseCommand
from travel.models import Country, Attraction, RestaurantPhrase, DishesToAvoid

class Command(BaseCommand):
    help = 'Ensure all travel data is properly migrated and populated'

    def handle(self, *args, **options):
        self.stdout.write('Ensuring travel data is properly migrated...')
        
        # Create or update countries with proper data
        countries_data = [
            {
                'name': 'Spain',
                'code': 'ES',
                'language': 'Spanish',
                'language_code': 'es',
                'flag_emoji': '🇪🇸',
                'celiac_awareness': 4,
                'summary': 'Spain has a growing awareness of celiac disease with many restaurants offering gluten-free options. Traditional Spanish cuisine includes many naturally gluten-free dishes.',
                'dining_tips': 'Look for "sin gluten" labels. Many tapas are naturally gluten-free. Paella is usually safe but ask about the broth. Avoid croquettes and breaded items.'
            },
            {
                'name': 'Germany',
                'code': 'DE',
                'language': 'German',
                'language_code': 'de',
                'flag_emoji': '🇩🇪',
                'celiac_awareness': 5,
                'summary': 'Germany has excellent celiac awareness with strict labeling laws. Many restaurants have dedicated gluten-free menus.',
                'dining_tips': 'Look for "glutenfrei" labels. Many German restaurants have gluten-free options. Avoid traditional breads and pretzels. Sausages may contain fillers.'
            },
            {
                'name': 'India',
                'code': 'IN',
                'language': 'Hindi',
                'language_code': 'hi',
                'flag_emoji': '🇮🇳',
                'celiac_awareness': 2,
                'summary': 'Celiac awareness is growing in India, especially in urban areas. Many traditional dishes are naturally gluten-free.',
                'dining_tips': 'Rice-based dishes are usually safe. Avoid wheat-based breads like naan and roti. Many curries are naturally gluten-free. Be careful with sauces and gravies.'
            },
            {
                'name': 'South Korea',
                'code': 'KR',
                'language': 'Korean',
                'language_code': 'ko',
                'flag_emoji': '🇰🇷',
                'celiac_awareness': 3,
                'summary': 'Celiac awareness is moderate in South Korea. Many traditional dishes use rice and are naturally gluten-free.',
                'dining_tips': 'Rice-based dishes are safe. Avoid wheat noodles and bread. Many Korean BBQ dishes are gluten-free. Be careful with soy sauce and marinades.'
            },
            {
                'name': 'Japan',
                'code': 'JP',
                'language': 'Japanese',
                'language_code': 'ja',
                'flag_emoji': '🇯🇵',
                'celiac_awareness': 3,
                'summary': 'Celiac awareness is growing in Japan. Many traditional dishes use rice and are naturally gluten-free.',
                'dining_tips': 'Sushi and sashimi are usually safe. Avoid wheat noodles like ramen and udon. Many Japanese restaurants have gluten-free options. Be careful with soy sauce.'
            },
            {
                'name': 'Saudi Arabia',
                'code': 'SA',
                'language': 'Arabic',
                'language_code': 'ar',
                'flag_emoji': '🇸🇦',
                'celiac_awareness': 2,
                'summary': 'Celiac awareness is developing in Saudi Arabia. Many Middle Eastern dishes are naturally gluten-free.',
                'dining_tips': 'Rice and grilled meats are usually safe. Avoid wheat-based breads. Many Middle Eastern dishes are naturally gluten-free. Be careful with sauces and marinades.'
            },
            {
                'name': 'Russia',
                'code': 'RU',
                'language': 'Russian',
                'language_code': 'ru',
                'flag_emoji': '🇷🇺',
                'celiac_awareness': 2,
                'summary': 'Celiac awareness is growing in Russia. Many traditional dishes can be adapted to be gluten-free.',
                'dining_tips': 'Look for "без глютена" labels. Many Russian dishes can be made gluten-free. Avoid traditional breads and pastries. Be careful with sauces and gravies.'
            },
            {
                'name': 'United States',
                'code': 'US',
                'language': 'English',
                'language_code': 'en',
                'flag_emoji': '🇺🇸',
                'celiac_awareness': 5,
                'summary': 'The US has excellent celiac awareness with strict labeling laws and many gluten-free options available.',
                'dining_tips': 'Look for "gluten-free" labels. Many restaurants have dedicated gluten-free menus. Chain restaurants often have gluten-free options. Be careful with cross-contamination.'
            },
            {
                'name': 'Portugal',
                'code': 'PT',
                'language': 'Portuguese',
                'language_code': 'pt',
                'flag_emoji': '🇵🇹',
                'celiac_awareness': 4,
                'summary': 'Portugal has good celiac awareness with many restaurants offering gluten-free options.',
                'dining_tips': 'Look for "sem glúten" labels. Many Portuguese dishes are naturally gluten-free. Seafood dishes are usually safe. Avoid bread and pastries.'
            },
            {
                'name': 'Italy',
                'code': 'IT',
                'language': 'Italian',
                'language_code': 'it',
                'flag_emoji': '🇮🇹',
                'celiac_awareness': 5,
                'summary': 'Italy has excellent celiac awareness with strict laws and many gluten-free options available.',
                'dining_tips': 'Look for "senza glutine" labels. Many Italian restaurants have gluten-free pasta. Risotto is usually safe. Avoid traditional bread and pizza.'
            },
            {
                'name': 'China',
                'code': 'CN',
                'language': 'Chinese',
                'language_code': 'zh',
                'flag_emoji': '🇨🇳',
                'celiac_awareness': 2,
                'summary': 'Celiac awareness is growing in China. Many traditional dishes use rice and are naturally gluten-free.',
                'dining_tips': 'Rice-based dishes are usually safe. Avoid wheat noodles and dumplings. Many stir-fry dishes are gluten-free. Be careful with soy sauce and sauces.'
            },
            {
                'name': 'France',
                'code': 'FR',
                'language': 'French',
                'language_code': 'fr',
                'flag_emoji': '🇫🇷',
                'celiac_awareness': 4,
                'summary': 'France has good celiac awareness with many restaurants offering gluten-free options.',
                'dining_tips': 'Look for "sans gluten" labels. Many French restaurants have gluten-free options. Avoid bread and pastries. Be careful with sauces and gravies.'
            }
        ]

        for country_data in countries_data:
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

        # Add sample attractions for each country
        attractions_data = {
            'Spain': [
                {
                    'name': 'Sagrada Familia',
                    'local_name': 'Basílica de la Sagrada Familia',
                    'description': 'Famous church designed by Antoni Gaudí, a UNESCO World Heritage site.',
                    'category': 'religious',
                    'gluten_free_info': 'Several gluten-free cafes nearby in the Eixample district.'
                },
                {
                    'name': 'Alhambra',
                    'local_name': 'Alhambra',
                    'description': 'Stunning Moorish palace complex in Granada.',
                    'category': 'monument',
                    'gluten_free_info': 'Restaurant on site offers gluten-free options.'
                }
            ],
            'Germany': [
                {
                    'name': 'Neuschwanstein Castle',
                    'local_name': 'Schloss Neuschwanstein',
                    'description': 'Fairy-tale castle that inspired Disney\'s Sleeping Beauty castle.',
                    'category': 'monument',
                    'gluten_free_info': 'Cafe nearby has gluten-free pastries and bread.'
                },
                {
                    'name': 'Brandenburg Gate',
                    'local_name': 'Brandenburger Tor',
                    'description': 'Historic gate and symbol of Berlin.',
                    'category': 'landmark',
                    'gluten_free_info': 'Many gluten-free restaurants in the surrounding area.'
                }
            ],
            'Italy': [
                {
                    'name': 'Colosseum',
                    'local_name': 'Colosseo',
                    'description': 'Ancient amphitheater and symbol of Rome.',
                    'category': 'monument',
                    'gluten_free_info': 'Many gluten-free restaurants in the area, including dedicated celiac-friendly establishments.'
                },
                {
                    'name': 'Leaning Tower of Pisa',
                    'local_name': 'Torre di Pisa',
                    'description': 'Famous leaning bell tower in Pisa.',
                    'category': 'monument',
                    'gluten_free_info': 'Several gluten-free restaurants in Pisa city center.'
                }
            ]
        }

        for country_name, attractions in attractions_data.items():
            country = Country.objects.get(name=country_name)
            for attraction_data in attractions:
                attraction, created = Attraction.objects.get_or_create(
                    country=country,
                    name=attraction_data['name'],
                    defaults=attraction_data
                )
                if created:
                    self.stdout.write(f'Created attraction: {attraction.name} in {country.name}')

        # Add sample phrases for each country
        phrases_data = {
            'Spain': {
                'general': [
                    {
                        'english_text': 'I have celiac disease',
                        'translated_text': 'Tengo enfermedad celíaca',
                        'pronunciation': 'TEN-go en-fer-meh-DAD seh-lee-AH-ka'
                    },
                    {
                        'english_text': 'I cannot eat gluten',
                        'translated_text': 'No puedo comer gluten',
                        'pronunciation': 'No PWEH-do ko-MER GLOO-ten'
                    }
                ],
                'ordering': [
                    {
                        'english_text': 'Is this gluten-free?',
                        'translated_text': '¿Esto es sin gluten?',
                        'pronunciation': 'EHS-to es seen GLOO-ten'
                    }
                ]
            },
            'Germany': {
                'general': [
                    {
                        'english_text': 'I have celiac disease',
                        'translated_text': 'Ich habe Zöliakie',
                        'pronunciation': 'Ikh HAH-beh tsoh-lee-ah-KEE'
                    },
                    {
                        'english_text': 'I cannot eat gluten',
                        'translated_text': 'Ich kann kein Gluten essen',
                        'pronunciation': 'Ikh kahn kine GLOO-ten ES-sen'
                    }
                ],
                'ordering': [
                    {
                        'english_text': 'Is this gluten-free?',
                        'translated_text': 'Ist das glutenfrei?',
                        'pronunciation': 'Ist dahs GLOO-ten-fry'
                    }
                ]
            },
            'Italy': {
                'general': [
                    {
                        'english_text': 'I have celiac disease',
                        'translated_text': 'Ho la celiachia',
                        'pronunciation': 'Oh lah cheh-lee-AH-kee-ah'
                    },
                    {
                        'english_text': 'I cannot eat gluten',
                        'translated_text': 'Non posso mangiare glutine',
                        'pronunciation': 'Non POS-so man-jah-reh gloo-TEE-neh'
                    }
                ],
                'ordering': [
                    {
                        'english_text': 'Is this gluten-free?',
                        'translated_text': 'È senza glutine?',
                        'pronunciation': 'Eh SEN-zah gloo-TEE-neh'
                    }
                ]
            }
        }

        for country_name, categories in phrases_data.items():
            country = Country.objects.get(name=country_name)
            for category, phrases in categories.items():
                for phrase_data in phrases:
                    phrase, created = RestaurantPhrase.objects.get_or_create(
                        country=country,
                        english_text=phrase_data['english_text'],
                        category=category,
                        defaults=phrase_data
                    )
                    if created:
                        self.stdout.write(f'Created phrase: {phrase.english_text} in {country.name}')

        self.stdout.write(self.style.SUCCESS('Successfully ensured all travel data is properly migrated!')) 