from django.db import migrations
from django.utils.text import slugify

def add_ecard_countries(apps, schema_editor):
    Country = apps.get_model('travel', 'Country')
    DishesToAvoid = apps.get_model('travel', 'DishesToAvoid')
    RestaurantPhrase = apps.get_model('travel', 'RestaurantPhrase')
    Attraction = apps.get_model('travel', 'Attraction')

    # Countries data for e-card language support
    countries_data = {
        'Portugal': {
            'code': 'PT',
            'flag_emoji': '🇵🇹',
            'language': 'Portuguese',
            'language_code': 'pt',
            'celiac_awareness': 3,
            'color': '#006600',
            'summary': 'Portugal has moderate celiac awareness with growing gluten-free options in major cities. Traditional rice and seafood dishes are naturally safe.',
            'dining_tips': 'Look for "sem glúten" labels. Many traditional dishes like grilled fish and rice are naturally gluten-free.',
            'dishes': [
                {
                    'name': 'Francesinha',
                    'local_name': 'Francesinha',
                    'description': 'Sandwich with bread and beer sauce containing gluten',
                    'ingredients': 'Wheat bread, beer sauce'
                },
                {
                    'name': 'Pastéis de Nata',
                    'local_name': 'Pastéis de Nata',
                    'description': 'Custard tarts with wheat flour pastry',
                    'ingredients': 'Wheat flour pastry'
                }
            ],
            'attractions': [
                {
                    'name': 'Tower of Belém',
                    'local_name': 'Torre de Belém',
                    'description': 'Historic fortress and UNESCO World Heritage site',
                    'category': 'monument',
                    'gluten_free_info': 'Nearby Belém district has gluten-free pastry shops'
                },
                {
                    'name': 'Pena Palace',
                    'local_name': 'Palácio da Pena',
                    'description': 'Romantic palace in Sintra mountains',
                    'category': 'cultural',
                    'gluten_free_info': 'Sintra town offers several gluten-free dining options'
                }
            ]
        },
        'China': {
            'code': 'CN',
            'flag_emoji': '🇨🇳',
            'language': 'Chinese',
            'language_code': 'zh',
            'celiac_awareness': 2,
            'color': '#DE2910',
            'summary': 'China has limited celiac awareness, but rice-based dishes are abundant. Soy sauce and wheat noodles are common, so careful ordering is essential.',
            'dining_tips': 'Ask for "无麸质" (gluten-free). Rice dishes and hot pot can be safe options with careful ingredient selection.',
            'dishes': [
                {
                    'name': 'Dumplings',
                    'local_name': '饺子',
                    'description': 'Wheat flour wrappers contain gluten',
                    'ingredients': 'Wheat flour wrappers'
                },
                {
                    'name': 'Noodles',
                    'local_name': '面条',
                    'description': 'Most Chinese noodles are made from wheat',
                    'ingredients': 'Wheat flour'
                },
                {
                    'name': 'Soy Sauce',
                    'local_name': '生抽',
                    'description': 'Traditional soy sauce contains wheat',
                    'ingredients': 'Soybeans, wheat'
                }
            ],
            'attractions': [
                {
                    'name': 'Great Wall of China',
                    'local_name': '长城',
                    'description': 'Ancient fortification and world wonder',
                    'category': 'monument',
                    'gluten_free_info': 'Tourist areas have limited but growing gluten-free options'
                },
                {
                    'name': 'Forbidden City',
                    'local_name': '紫禁城',
                    'description': 'Imperial palace complex in Beijing',
                    'category': 'cultural',
                    'gluten_free_info': 'Beijing has international restaurants with gluten-free menus'
                }
            ]
        },
        'South Korea': {
            'code': 'KR',
            'flag_emoji': '🇰🇷',
            'language': 'Korean',
            'language_code': 'ko',
            'celiac_awareness': 2,
            'color': '#003478',
            'summary': 'South Korea has growing awareness of gluten-free needs. Rice is a staple, but many sauces and seasonings contain wheat.',
            'dining_tips': 'Look for "글루텐 프리" labels. Korean BBQ and rice dishes can be safe with careful sauce selection.',
            'dishes': [
                {
                    'name': 'Kimchi Jjigae',
                    'local_name': '김치찌개',
                    'description': 'May contain wheat-based seasonings',
                    'ingredients': 'Sometimes contains wheat-based soy sauce'
                },
                {
                    'name': 'Bulgogi',
                    'local_name': '불고기',
                    'description': 'Marinade often contains soy sauce with wheat',
                    'ingredients': 'Soy sauce marinade with wheat'
                }
            ],
            'attractions': [
                {
                    'name': 'Gyeongbokgung Palace',
                    'local_name': '경복궁',
                    'description': 'Main royal palace of Joseon dynasty',
                    'category': 'cultural',
                    'gluten_free_info': 'Seoul has many international restaurants with gluten-free options'
                },
                {
                    'name': 'Jeju Island',
                    'local_name': '제주도',
                    'description': 'Volcanic island with natural beauty',
                    'category': 'landmark',
                    'gluten_free_info': 'Resort areas cater to international dietary needs'
                }
            ]
        },
        'Saudi Arabia': {
            'code': 'SA',
            'flag_emoji': '🇸🇦',
            'language': 'Arabic',
            'language_code': 'ar',
            'celiac_awareness': 3,
            'color': '#006C35',
            'summary': 'Saudi Arabia has moderate celiac awareness with international dining options in major cities. Rice and grilled meats are traditional safe options.',
            'dining_tips': 'Ask for "خالي من الغلوتين" (gluten-free). Traditional rice dishes and grilled meats are usually safe.',
            'dishes': [
                {
                    'name': 'Shawarma',
                    'local_name': 'شاورما',
                    'description': 'Served in wheat pita bread',
                    'ingredients': 'Wheat pita bread'
                },
                {
                    'name': 'Kuboos',
                    'local_name': 'خبز',
                    'description': 'Traditional Arabic bread made with wheat',
                    'ingredients': 'Wheat flour'
                }
            ],
            'attractions': [
                {
                    'name': 'Masjid al-Haram',
                    'local_name': 'المسجد الحرام',
                    'description': 'Holiest mosque in Islam in Mecca',
                    'category': 'religious',
                    'gluten_free_info': 'Mecca has international hotels with dietary accommodations'
                },
                {
                    'name': 'Al-Ula',
                    'local_name': 'العلا',
                    'description': 'Ancient archaeological site with rock formations',
                    'category': 'cultural',
                    'gluten_free_info': 'Tourist facilities provide international dining options'
                }
            ]
        },
        'Russia': {
            'code': 'RU',
            'flag_emoji': '🇷🇺',
            'language': 'Russian',
            'language_code': 'ru',
            'celiac_awareness': 2,
            'color': '#0039A6',
            'summary': 'Russia has limited celiac awareness, but major cities offer some gluten-free options. Traditional buckwheat dishes are naturally safe.',
            'dining_tips': 'Look for "без глютена" labels. Buckwheat dishes and grilled meats are traditional safe options.',
            'dishes': [
                {
                    'name': 'Borscht',
                    'local_name': 'Борщ',
                    'description': 'May be thickened with wheat flour',
                    'ingredients': 'Sometimes contains wheat flour'
                },
                {
                    'name': 'Blini',
                    'local_name': 'Блины',
                    'description': 'Pancakes made with wheat flour',
                    'ingredients': 'Wheat flour'
                }
            ],
            'attractions': [
                {
                    'name': 'Red Square',
                    'local_name': 'Красная площадь',
                    'description': 'Historic square in Moscow',
                    'category': 'landmark',
                    'gluten_free_info': 'Moscow has growing number of gluten-free restaurants'
                },
                {
                    'name': 'Hermitage Museum',
                    'local_name': 'Эрмитаж',
                    'description': 'World-famous art museum in St. Petersburg',
                    'category': 'museum',
                    'gluten_free_info': 'St. Petersburg offers some international dining with gluten-free options'
                }
            ]
        },
        'India': {
            'code': 'IN',
            'flag_emoji': '🇮🇳',
            'language': 'Hindi',
            'language_code': 'hi',
            'celiac_awareness': 2,
            'color': '#FF9933',
            'summary': 'India has limited celiac awareness, but rice-based dishes are abundant. Wheat flatbreads are very common, so careful ordering is essential.',
            'dining_tips': 'Ask for "ग्लूटेन मुक्त" (gluten-free). Rice dishes, dal, and many curries can be safe options.',
            'dishes': [
                {
                    'name': 'Roti',
                    'local_name': 'रोटी',
                    'description': 'Flatbread made from wheat flour',
                    'ingredients': 'Wheat flour'
                },
                {
                    'name': 'Naan',
                    'local_name': 'नान',
                    'description': 'Leavened bread made with wheat flour',
                    'ingredients': 'Wheat flour, yeast'
                },
                {
                    'name': 'Samosa',
                    'local_name': 'समोसा',
                    'description': 'Fried pastry with wheat flour wrapper',
                    'ingredients': 'Wheat flour wrapper'
                }
            ],
            'attractions': [
                {
                    'name': 'Taj Mahal',
                    'local_name': 'ताज महल',
                    'description': 'Iconic marble mausoleum in Agra',
                    'category': 'monument',
                    'gluten_free_info': 'Agra has hotels with international cuisine and dietary accommodations'
                },
                {
                    'name': 'Red Fort',
                    'local_name': 'लाल किला',
                    'description': 'Historic fortified palace in Delhi',
                    'category': 'monument',
                    'gluten_free_info': 'Delhi offers diverse dining with some gluten-free options'
                }
            ]
        }
    }

    # Create countries
    for country_name, data in countries_data.items():
        # Generate unique slug
        base_slug = slugify(country_name)
        slug = base_slug
        counter = 1
        while Country.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
            
        country, created = Country.objects.get_or_create(
            name=country_name,
            defaults={
                'slug': slug,
                'code': data['code'],
                'flag_emoji': data['flag_emoji'],
                'language': data['language'],
                'language_code': data['language_code'],
                'celiac_awareness': data['celiac_awareness'],
                'color': data['color'],
                'summary': data['summary'],
                'dining_tips': data['dining_tips']
            }
        )
        
        if created:
            # Add dishes to avoid
            for dish_data in data['dishes']:
                DishesToAvoid.objects.create(
                    country=country,
                    name=dish_data['name'],
                    local_name=dish_data['local_name'],
                    description=dish_data['description'],
                    ingredients=dish_data['ingredients']
                )

            # Add attractions
            for attraction_data in data['attractions']:
                Attraction.objects.create(
                    country=country,
                    name=attraction_data['name'],
                    local_name=attraction_data['local_name'],
                    description=attraction_data['description'],
                    category=attraction_data['category'],
                    gluten_free_info=attraction_data['gluten_free_info']
                )

            # Add basic restaurant phrases
            phrases = [
                {
                    'category': 'general',
                    'english_text': 'I have celiac disease',
                    'translated_text': 'Translation needed',
                    'pronunciation': 'Pronunciation needed'
                },
                {
                    'category': 'ordering',
                    'english_text': 'Do you have gluten-free options?',
                    'translated_text': 'Translation needed',
                    'pronunciation': 'Pronunciation needed'
                },
                {
                    'category': 'ingredients',
                    'english_text': 'Does this contain wheat, barley, or rye?',
                    'translated_text': 'Translation needed',
                    'pronunciation': 'Pronunciation needed'
                }
            ]
            
            for phrase_data in phrases:
                RestaurantPhrase.objects.create(
                    country=country,
                    category=phrase_data['category'],
                    english_text=phrase_data['english_text'],
                    translated_text=phrase_data['translated_text'],
                    pronunciation=phrase_data['pronunciation']
                )

def reverse_add_ecard_countries(apps, schema_editor):
    Country = apps.get_model('travel', 'Country')
    countries_to_remove = ['Portugal', 'China', 'South Korea', 'Saudi Arabia', 'Russia', 'India']
    Country.objects.filter(name__in=countries_to_remove).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0007_complete_country_data'),
    ]

    operations = [
        migrations.RunPython(add_ecard_countries, reverse_add_ecard_countries),
    ]