from django.core.management.base import BaseCommand
from django.db import transaction
from travel.models import Country, DishesToAvoid, RestaurantPhrase

class Command(BaseCommand):
    help = 'Populates the database with travel guide data for the top 10 most traveled countries'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write('Creating travel guide data...')
        
        # Clear existing data
        Country.objects.all().delete()
        
        # Create countries with useful celiac-related information
        countries_data = [
            {
                'name': 'Italy',
                'code': 'IT',
                'flag_emoji': '🇮🇹',
                'language': 'Italian',
                'language_code': 'it',
                'celiac_awareness': 5,
                'summary': 'Italy has excellent celiac awareness, with a high prevalence of celiac disease in the population (about 1%). The Italian Celiac Association (AIC) provides extensive support, and many restaurants are certified gluten-free. "Senza glutine" (gluten-free) options are widely available.',
                'dining_tips': 'Look for the "Alimentazione Fuori Casa" AIC certification logo which indicates restaurants trained in safe gluten-free food preparation. Many gelaterias have gluten-free cones, and pharmacies carry a wide range of gluten-free products. Pizza and pasta establishments often offer gluten-free options but confirm separate preparation areas.'
            },
            {
                'name': 'France',
                'code': 'FR',
                'flag_emoji': '🇫🇷',
                'language': 'French',
                'language_code': 'fr',
                'celiac_awareness': 3,
                'summary': 'France has moderate celiac awareness. While traditional French cuisine relies heavily on bread and pastries, larger cities like Paris offer numerous gluten-free options. The French Celiac Association (AFDIAG) provides restaurant cards and resources.',
                'dining_tips': 'Look for "sans gluten" offerings, particularly in larger cities. Be cautious about cross-contamination when ordering crêpes, as most establishments use the same surfaces. French pharmacies typically stock gluten-free products. Consider apartments with kitchens for longer stays to prepare your own meals.'
            },
            {
                'name': 'Spain',
                'code': 'ES',
                'flag_emoji': '🇪🇸',
                'language': 'Spanish',
                'language_code': 'es',
                'celiac_awareness': 4,
                'summary': 'Spain has good celiac awareness with strong advocacy from FACE (Federación de Asociaciones de Celiacos de España). Many restaurants display the "Sin Gluten" logo, indicating they follow protocols for safe gluten-free preparation.',
                'dining_tips': 'Spanish staples like tortilla española (potato omelette) and paella are traditionally gluten-free, but always verify preparation methods. Avoid croquetas and empanadas. Many restaurants have dedicated gluten-free menus, especially in major cities and tourist areas. Mercadona supermarkets offer extensive gluten-free sections.'
            },
            {
                'name': 'United States',
                'code': 'US',
                'flag_emoji': '🇺🇸',
                'language': 'English',
                'language_code': 'en',
                'celiac_awareness': 4,
                'summary': 'The United States has high celiac awareness with strong advocacy organizations. Gluten-free options are widely available in grocery stores and restaurants, though quality and safety vary significantly between establishments.',
                'dining_tips': 'Chain restaurants often have standardized gluten-free menus. Apps like Find Me Gluten Free are particularly useful. Always specify "celiac" rather than just "gluten-free" as some establishments treat preferences differently from medical necessities. Dedicated gluten-free restaurants and bakeries are common in larger cities.'
            },
            {
                'name': 'Japan',
                'code': 'JP',
                'flag_emoji': '🇯🇵',
                'language': 'Japanese',
                'language_code': 'ja',
                'celiac_awareness': 2,
                'summary': 'Japan has limited celiac awareness as the condition is rare in the Japanese population. Soy sauce (which contains wheat) is ubiquitous in Japanese cuisine, making dining challenging. Language barriers can further complicate explaining dietary restrictions.',
                'dining_tips': 'Pure sushi with just fish and rice is generally safe, but confirm no soy sauce is added. Traditional Japanese rice dishes without sauce can be safe options. Carry gluten-free soy sauce packets for your own use. Consider booking hotels with refrigerators to store safe snacks and breakfast items.'
            }
        ]
        
        # Create countries
        for country_data in countries_data:
            country = Country.objects.create(**country_data)
            self.stdout.write(f'Created country: {country.name}')
            
            # Add dishes to avoid for each country
            self._add_dishes_to_avoid(country)
            
            # Add restaurant phrases for each country
            self._add_restaurant_phrases(country)
            
        self.stdout.write(self.style.SUCCESS('Successfully created travel guide data!'))
    
    def _add_dishes_to_avoid(self, country):
        """Add dishes to avoid based on country"""
        dishes_data = {
            'IT': [
                {
                    'name': 'Regular Pasta',
                    'local_name': 'Pasta',
                    'description': 'Traditional pasta made from wheat flour',
                    'ingredients': 'Wheat flour, sometimes eggs'
                },
                {
                    'name': 'Regular Pizza',
                    'local_name': 'Pizza',
                    'description': 'Traditional pizza with wheat-based crust',
                    'ingredients': 'Wheat flour, yeast'
                },
                {
                    'name': 'Panettone',
                    'local_name': 'Panettone',
                    'description': 'Traditional Italian Christmas cake',
                    'ingredients': 'Wheat flour, candied fruits, raisins'
                }
            ],
            'FR': [
                {
                    'name': 'Croissant',
                    'local_name': 'Croissant',
                    'description': 'Flaky, buttery pastry',
                    'ingredients': 'Wheat flour, butter, yeast'
                },
                {
                    'name': 'Baguette',
                    'local_name': 'Baguette',
                    'description': 'Long, thin loaf of French bread',
                    'ingredients': 'Wheat flour, yeast, salt'
                },
                {
                    'name': 'Crêpes',
                    'local_name': 'Crêpes',
                    'description': 'Thin pancakes served with various fillings',
                    'ingredients': 'Wheat flour, milk, eggs'
                }
            ],
            'ES': [
                {
                    'name': 'Empanadillas',
                    'local_name': 'Empanadillas',
                    'description': 'Small, stuffed pastries',
                    'ingredients': 'Wheat flour, various fillings'
                },
                {
                    'name': 'Croquetas',
                    'local_name': 'Croquetas',
                    'description': 'Breaded and fried roll with filling',
                    'ingredients': 'Wheat flour, breadcrumbs, filling'
                },
                {
                    'name': 'Churros',
                    'local_name': 'Churros',
                    'description': 'Fried dough pastry served with chocolate',
                    'ingredients': 'Wheat flour, oil'
                }
            ],
            'US': [
                {
                    'name': 'Fried Chicken',
                    'local_name': 'Fried Chicken',
                    'description': 'Chicken coated in seasoned flour and deep-fried',
                    'ingredients': 'Wheat flour, spices'
                },
                {
                    'name': 'Burger with Bun',
                    'local_name': 'Hamburger',
                    'description': 'Ground beef patty served in a wheat bun',
                    'ingredients': 'Wheat bun, meat, various toppings'
                },
                {
                    'name': 'Mac and Cheese',
                    'local_name': 'Macaroni and Cheese',
                    'description': 'Pasta with cheese sauce',
                    'ingredients': 'Wheat pasta, cheese, sometimes flour-based sauce'
                }
            ],
            'JP': [
                {
                    'name': 'Tempura',
                    'local_name': '天ぷら',
                    'description': 'Battered and deep-fried seafood or vegetables',
                    'ingredients': 'Wheat flour batter'
                },
                {
                    'name': 'Ramen',
                    'local_name': 'ラーメン',
                    'description': 'Noodle soup dish',
                    'ingredients': 'Wheat noodles, broth (often contains soy sauce)'
                },
                {
                    'name': 'Katsu',
                    'local_name': 'カツ',
                    'description': 'Breaded cutlet of meat',
                    'ingredients': 'Breadcrumbs (panko), meat, sometimes flour'
                }
            ]
        }
        
        if country.code in dishes_data:
            for dish_data in dishes_data[country.code]:
                DishesToAvoid.objects.create(country=country, **dish_data)
                self.stdout.write(f'Added dish to avoid for {country.name}: {dish_data["name"]}')
    
    def _add_restaurant_phrases(self, country):
        """Add restaurant phrases based on country"""
        # General phrases for all countries
        general_phrases = [
            {
                'category': 'general',
                'english_text': 'I have celiac disease. I cannot eat gluten.',
                'translations': {
                    'IT': 'Ho la celiachia. Non posso mangiare glutine.',
                    'FR': 'Je suis atteint(e) de la maladie cœliaque. Je ne peux pas manger de gluten.',
                    'ES': 'Tengo enfermedad celíaca. No puedo comer gluten.',
                    'US': 'I have celiac disease. I cannot eat gluten.',
                    'JP': '私はセリアック病です。グルテンを食べることができません。'
                }
            },
            {
                'category': 'general',
                'english_text': 'Is this food gluten-free?',
                'translations': {
                    'IT': 'Questo cibo è senza glutine?',
                    'FR': 'Cette nourriture est-elle sans gluten?',
                    'ES': '¿Esta comida es sin gluten?',
                    'US': 'Is this food gluten-free?',
                    'JP': 'この食べ物はグルテンフリーですか？'
                }
            }
        ]
        
        # Add general phrases
        for phrase_data in general_phrases:
            if country.code in phrase_data['translations']:
                RestaurantPhrase.objects.create(
                    country=country,
                    category=phrase_data['category'],
                    english_text=phrase_data['english_text'],
                    translated_text=phrase_data['translations'][country.code]
                )
        
        # Add country-specific ordering phrases
        ordering_phrases = [
            {
                'category': 'ordering',
                'english_text': 'Can you prepare this without gluten?',
                'translations': {
                    'IT': 'Potete preparare questo senza glutine?',
                    'FR': 'Pouvez-vous préparer ceci sans gluten?',
                    'ES': '¿Pueden preparar esto sin gluten?',
                    'US': 'Can you prepare this without gluten?',
                    'JP': 'グルテンなしでこれを準備できますか？'
                }
            }
        ]
        
        # Add ordering phrases
        for phrase_data in ordering_phrases:
            if country.code in phrase_data['translations']:
                RestaurantPhrase.objects.create(
                    country=country,
                    category=phrase_data['category'],
                    english_text=phrase_data['english_text'],
                    translated_text=phrase_data['translations'][country.code]
                )
                
        # Add country-specific ingredient phrases
        ingredient_phrases = [
            {
                'category': 'ingredients',
                'english_text': 'Does this contain wheat, barley, or rye?',
                'translations': {
                    'IT': 'Contiene frumento, orzo o segale?',
                    'FR': 'Est-ce que cela contient du blé, de l\'orge ou du seigle?',
                    'ES': '¿Contiene trigo, cebada o centeno?',
                    'US': 'Does this contain wheat, barley, or rye?',
                    'JP': 'これには小麦、大麦、またはライ麦が含まれていますか？'
                }
            }
        ]
        
        # Add ingredient phrases
        for phrase_data in ingredient_phrases:
            if country.code in phrase_data['translations']:
                RestaurantPhrase.objects.create(
                    country=country,
                    category=phrase_data['category'],
                    english_text=phrase_data['english_text'],
                    translated_text=phrase_data['translations'][country.code]
                )
