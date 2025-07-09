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
            },
            {
                'name': 'South Korea',
                'code': 'KR',
                'flag_emoji': '🇰🇷',
                'language': 'Korean',
                'language_code': 'ko',
                'celiac_awareness': 2,
                'summary': 'South Korea has limited celiac awareness as celiac disease is rare in the Korean population. Korean cuisine heavily features wheat-based noodles, soy sauce, and fermented products that may contain gluten. Language barriers can make communication challenging.',
                'dining_tips': 'Rice-based dishes like bibimbap (without sauce) can be safer options. Be cautious with kimchi as some varieties contain wheat flour. Korean BBQ meat without marinades is generally safe. Consider staying in accommodations with kitchen facilities and shop at international supermarkets for gluten-free products.'
            },
            {
                'name': 'Saudi Arabia',
                'code': 'SA',
                'flag_emoji': '🇸🇦',
                'language': 'Arabic',
                'language_code': 'ar',
                'celiac_awareness': 3,
                'summary': 'Saudi Arabia has moderate celiac awareness, particularly in major cities like Riyadh and Jeddah. Traditional Middle Eastern cuisine includes many wheat-based items, but rice dishes and grilled meats are common alternatives.',
                'dining_tips': 'Rice-based dishes like kabsa are typically safe. Grilled meats and vegetables without marinades are good options. Be cautious with traditional breads and pastries. International hotels and restaurants in major cities are more likely to understand gluten-free requirements. Carry translation cards in Arabic.'
            },
            {
                'name': 'Russia',
                'code': 'RU',
                'flag_emoji': '🇷🇺',
                'language': 'Russian',
                'language_code': 'ru',
                'celiac_awareness': 2,
                'summary': 'Russia has limited celiac awareness, though it is improving in major cities like Moscow and St. Petersburg. Traditional Russian cuisine relies heavily on bread, wheat-based soups, and pasta dishes.',
                'dining_tips': 'Focus on simple grilled meats, fish, and vegetables. Traditional buckwheat dishes (grechka) are naturally gluten-free. Be cautious with soups as many contain flour thickeners. International restaurants and hotels in major cities may have better understanding of dietary restrictions.'
            },
            {
                'name': 'India',
                'code': 'IN',
                'flag_emoji': '🇮🇳',
                'language': 'Hindi',
                'language_code': 'hi',
                'celiac_awareness': 2,
                'summary': 'India has limited celiac awareness, though rice-based dishes in South India and naturally gluten-free options like dal and vegetables are abundant. Wheat-based breads (roti, naan) are staples in North Indian cuisine.',
                'dining_tips': 'South Indian cuisine with rice-based dishes is generally safer. Plain rice, dal (lentils), and vegetable curries are typically gluten-free. Avoid wheat-based breads and be cautious with spice mixes that may contain wheat flour. Communicate dietary needs clearly as cross-contamination is common in kitchens.'
            },
            {
                'name': 'Australia',
                'code': 'AU',
                'flag_emoji': '🇦🇺',
                'language': 'English',
                'language_code': 'en',
                'celiac_awareness': 5,
                'summary': 'Australia has very high level of celiac awareness, supported by Coeliac Australia. The country has excellent gluten-free labeling laws and widespread availability of certified gluten-free products in supermarkets and restaurants.',
                'dining_tips': 'Look for certified gluten-free products with the crossed grain symbol. Major supermarket chains like Woolworths and Coles have extensive gluten-free sections. Many restaurants offer gluten-free menus, and staff are generally well-trained about cross-contamination. Australian cafes often have gluten-free bread and cake options.'
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
            ],
            'KR': [
                {
                    'name': 'Jjajangmyeon',
                    'local_name': '짜장면',
                    'description': 'Noodles with black bean sauce',
                    'ingredients': 'Wheat noodles, black bean sauce'
                },
                {
                    'name': 'Mandu',
                    'local_name': '만두',
                    'description': 'Korean dumplings',
                    'ingredients': 'Wheat flour wrapper, various fillings'
                },
                {
                    'name': 'Korean Fried Chicken',
                    'local_name': '치킨',
                    'description': 'Crispy fried chicken with coating',
                    'ingredients': 'Wheat flour coating, chicken'
                }
            ],
            'SA': [
                {
                    'name': 'Shawarma Wrap',
                    'local_name': 'شاورما',
                    'description': 'Meat wrapped in flatbread',
                    'ingredients': 'Wheat flatbread, meat, vegetables'
                },
                {
                    'name': 'Falafel',
                    'local_name': 'فلافل',
                    'description': 'Deep-fried chickpea balls (often contains wheat)',
                    'ingredients': 'Chickpeas, sometimes wheat flour as binder'
                },
                {
                    'name': 'Kunafa',
                    'local_name': 'كنافة',
                    'description': 'Sweet pastry with cheese or cream',
                    'ingredients': 'Wheat-based pastry, cheese, syrup'
                }
            ],
            'RU': [
                {
                    'name': 'Borscht with Sour Cream',
                    'local_name': 'Борщ',
                    'description': 'Beet soup often thickened with flour',
                    'ingredients': 'Vegetables, sometimes flour as thickener'
                },
                {
                    'name': 'Blini',
                    'local_name': 'Блины',
                    'description': 'Thin pancakes',
                    'ingredients': 'Wheat flour, milk, eggs'
                },
                {
                    'name': 'Beef Stroganoff',
                    'local_name': 'Бефстроганов',
                    'description': 'Beef in sour cream sauce, often thickened with flour',
                    'ingredients': 'Beef, sour cream, often wheat flour'
                }
            ],
            'IN': [
                {
                    'name': 'Naan',
                    'local_name': 'नान',
                    'description': 'Leavened flatbread',
                    'ingredients': 'Wheat flour, yogurt, yeast'
                },
                {
                    'name': 'Roti/Chapati',
                    'local_name': 'रोटी/चपाती',
                    'description': 'Unleavened flatbread',
                    'ingredients': 'Wheat flour, water'
                },
                {
                    'name': 'Samosa',
                    'local_name': 'समोसा',
                    'description': 'Fried pastry with filling',
                    'ingredients': 'Wheat flour pastry, various fillings'
                }
            ],
            'AU': [
                {
                    'name': 'Meat Pie',
                    'local_name': 'Meat Pie',
                    'description': 'Traditional Australian pastry filled with meat',
                    'ingredients': 'Wheat flour pastry, meat filling'
                },
                {
                    'name': 'Lamington',
                    'local_name': 'Lamington',
                    'description': 'Sponge cake coated in chocolate and coconut',
                    'ingredients': 'Wheat flour, chocolate, coconut'
                },
                {
                    'name': 'Fish and Chips (battered)',
                    'local_name': 'Fish and Chips',
                    'description': 'Battered fish with chips',
                    'ingredients': 'Wheat flour batter, fish, potatoes'
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
                    'JP': '私はセリアック病です。グルテンを食べることができません。',
                    'KR': '저는 셀리악병이 있습니다. 글루텐을 먹을 수 없습니다.',
                    'SA': 'أعاني من مرض السيلياك. لا أستطيع أكل الغلوتين.',
                    'RU': 'У меня целиакия. Я не могу есть глютен.',
                    'IN': 'मुझे सीलिएक रोग है। मैं ग्लूटेन नहीं खा सकता।',
                    'AU': 'I have celiac disease. I cannot eat gluten.'
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
                    'JP': 'この食べ物はグルテンフリーですか？',
                    'KR': '이 음식은 글루텐 프리인가요?',
                    'SA': 'هل هذا الطعام خالي من الغلوتين؟',
                    'RU': 'Эта еда без глютена?',
                    'IN': 'क्या यह भोजन ग्लूटेन-फ्री है?',
                    'AU': 'Is this food gluten-free?'
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
                    'JP': 'グルテンなしでこれを準備できますか？',
                    'KR': '글루텐 없이 이것을 준비해 주실 수 있나요?',
                    'SA': 'هل يمكنكم تحضير هذا بدون غلوتين؟',
                    'RU': 'Можете ли вы приготовить это без глютена?',
                    'IN': 'क्या आप इसे ग्लूटेन के बिना तैयार कर सकते हैं?',
                    'AU': 'Can you prepare this without gluten?'
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
                    'JP': 'これには小麦、大麦、またはライ麦が含まれていますか？',
                    'KR': '이것에 밀, 보리, 또는 호밀이 들어있나요?',
                    'SA': 'هل يحتوي هذا على القمح أو الشعير أو الجاودار؟',
                    'RU': 'Содержит ли это пшеницу, ячмень или рожь?',
                    'IN': 'क्या इसमें गेहूं, जौ, या राई है?',
                    'AU': 'Does this contain wheat, barley, or rye?'
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
                
        # Add e-card message phrases
        message_phrases = [
            {
                'category': 'message',
                'english_text': 'I have celiac disease and cannot eat gluten. Please help me find safe food options.',
                'translations': {
                    'IT': 'Ho la celiachia e non posso mangiare glutine. Per favore aiutatemi a trovare opzioni alimentari sicure.',
                    'FR': 'Je suis atteint(e) de la maladie cœliaque et ne peux pas manger de gluten. Aidez-moi s\'il vous plaît à trouver des options alimentaires sûres.',
                    'ES': 'Tengo enfermedad celíaca y no puedo comer gluten. Por favor ayúdenme a encontrar opciones de comida segura.',
                    'US': 'I have celiac disease and cannot eat gluten. Please help me find safe food options.',
                    'JP': '私はセリアック病でグルテンを食べることができません。安全な食べ物の選択肢を見つけるのを手伝ってください。',
                    'KR': '저는 셀리악병이 있어서 글루텐을 먹을 수 없습니다. 안전한 음식 옵션을 찾는 것을 도와주세요.',
                    'SA': 'أعاني من مرض السيلياك ولا أستطيع أكل الغلوتين. من فضلكم ساعدوني في العثور على خيارات طعام آمنة.',
                    'RU': 'У меня целиакия, и я не могу есть глютен. Пожалуйста, помогите мне найти безопасные варианты питания.',
                    'IN': 'मुझे सीलिएक रोग है और मैं ग्लूटेन नहीं खा सकता। कृपया मुझे सुरक्षित भोजन विकल्प खोजने में मदद करें।',
                    'AU': 'I have celiac disease and cannot eat gluten. Please help me find safe food options.'
                }
            },
            {
                'category': 'message',
                'english_text': 'Emergency: I need gluten-free food immediately due to celiac disease.',
                'translations': {
                    'IT': 'Emergenza: Ho bisogno immediatamente di cibo senza glutine a causa della celiachia.',
                    'FR': 'Urgence: J\'ai besoin immédiatement de nourriture sans gluten à cause de la maladie cœliaque.',
                    'ES': 'Emergencia: Necesito comida sin gluten inmediatamente debido a la enfermedad celíaca.',
                    'US': 'Emergency: I need gluten-free food immediately due to celiac disease.',
                    'JP': '緊急事態：セリアック病のため、すぐにグルテンフリーの食べ物が必要です。',
                    'KR': '응급상황: 셀리악병 때문에 즉시 글루텐 프리 음식이 필요합니다.',
                    'SA': 'طوارئ: أحتاج إلى طعام خالي من الغلوتين فوراً بسبب مرض السيلياك.',
                    'RU': 'Экстренная ситуация: Мне срочно нужна еда без глютена из-за целиакии.',
                    'IN': 'आपातकाल: सीलिएक रोग के कारण मुझे तुरंत ग्लूटेन-फ्री भोजन की आवश्यकता है।',
                    'AU': 'Emergency: I need gluten-free food immediately due to celiac disease.'
                }
            }
        ]
        
        # Add message phrases
        for phrase_data in message_phrases:
            if country.code in phrase_data['translations']:
                RestaurantPhrase.objects.create(
                    country=country,
                    category=phrase_data['category'],
                    english_text=phrase_data['english_text'],
                    translated_text=phrase_data['translations'][country.code]
                )
