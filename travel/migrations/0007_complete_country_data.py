from django.db import migrations

def add_complete_country_data(apps, schema_editor):
    Country = apps.get_model('travel', 'Country')
    DishesToAvoid = apps.get_model('travel', 'DishesToAvoid')
    RestaurantPhrase = apps.get_model('travel', 'RestaurantPhrase')
    Attraction = apps.get_model('travel', 'Attraction')

    # Update existing countries with colors and complete data
    countries_data = {
        'Italy': {
            'color': '#228B22',
            'flag_emoji': '🇮🇹',
            'dishes': [
                {
                    'name': 'Pasta',
                    'local_name': 'Pasta',
                    'description': 'Traditional wheat-based pasta contains gluten',
                    'ingredients': 'Wheat flour, semolina'
                },
                {
                    'name': 'Pizza',
                    'local_name': 'Pizza',
                    'description': 'Traditional pizza dough contains wheat flour',
                    'ingredients': 'Wheat flour, yeast'
                },
                {
                    'name': 'Risotto',
                    'local_name': 'Risotto',
                    'description': 'Usually safe, but check for wheat-based stock',
                    'ingredients': 'May contain wheat-based broth'
                }
            ],
            'attractions': [
                {
                    'name': 'Colosseum',
                    'local_name': 'Colosseo',
                    'description': 'Ancient Roman amphitheater and iconic landmark',
                    'category': 'monument',
                    'gluten_free_info': 'Nearby restaurants offer gluten-free options'
                },
                {
                    'name': 'Vatican Museums',
                    'local_name': 'Musei Vaticani',
                    'description': 'World-renowned art collection and Sistine Chapel',
                    'category': 'museum',
                    'gluten_free_info': 'Cafeteria has some gluten-free options'
                },
                {
                    'name': 'Trevi Fountain',
                    'local_name': 'Fontana di Trevi',
                    'description': 'Famous baroque fountain in Rome',
                    'category': 'landmark',
                    'gluten_free_info': 'Many nearby gelaterias offer gluten-free options'
                }
            ]
        },
        'France': {
            'color': '#0055A4',
            'flag_emoji': '🇫🇷',
            'dishes': [
                {
                    'name': 'Baguette',
                    'local_name': 'Baguette',
                    'description': 'Traditional French bread contains wheat',
                    'ingredients': 'Wheat flour, yeast, salt'
                },
                {
                    'name': 'Croissant',
                    'local_name': 'Croissant',
                    'description': 'Buttery pastry made with wheat flour',
                    'ingredients': 'Wheat flour, butter, yeast'
                },
                {
                    'name': 'Coq au Vin',
                    'local_name': 'Coq au Vin',
                    'description': 'May be thickened with wheat flour',
                    'ingredients': 'Often contains wheat flour for thickening'
                }
            ],
            'attractions': [
                {
                    'name': 'Eiffel Tower',
                    'local_name': 'Tour Eiffel',
                    'description': 'Iconic iron lattice tower and symbol of Paris',
                    'category': 'landmark',
                    'gluten_free_info': 'Restaurant on second floor offers gluten-free menu'
                },
                {
                    'name': 'Louvre Museum',
                    'local_name': 'Musée du Louvre',
                    'description': 'World\'s largest art museum',
                    'category': 'museum',
                    'gluten_free_info': 'Café has limited gluten-free options'
                },
                {
                    'name': 'Notre-Dame Cathedral',
                    'local_name': 'Cathédrale Notre-Dame',
                    'description': 'Medieval Catholic cathedral',
                    'category': 'religious',
                    'gluten_free_info': 'Nearby cafés offer gluten-free pastries'
                }
            ]
        },
        'Japan': {
            'color': '#BC002D',
            'flag_emoji': '🇯🇵',
            'dishes': [
                {
                    'name': 'Ramen',
                    'local_name': 'ラーメン',
                    'description': 'Wheat-based noodles in broth',
                    'ingredients': 'Wheat noodles, soy sauce (may contain wheat)'
                },
                {
                    'name': 'Tempura',
                    'local_name': 'てんぷら',
                    'description': 'Battered and fried seafood/vegetables',
                    'ingredients': 'Wheat flour batter'
                },
                {
                    'name': 'Soy Sauce',
                    'local_name': '醤油',
                    'description': 'Traditional soy sauce contains wheat',
                    'ingredients': 'Soybeans, wheat, salt'
                }
            ],
            'attractions': [
                {
                    'name': 'Mount Fuji',
                    'local_name': '富士山',
                    'description': 'Sacred mountain and highest peak in Japan',
                    'category': 'landmark',
                    'gluten_free_info': 'Mountain huts have limited gluten-free options'
                },
                {
                    'name': 'Senso-ji Temple',
                    'local_name': '浅草寺',
                    'description': 'Ancient Buddhist temple in Tokyo',
                    'category': 'religious',
                    'gluten_free_info': 'Nearby restaurants offer rice-based dishes'
                },
                {
                    'name': 'Tokyo Imperial Palace',
                    'local_name': '皇居',
                    'description': 'Primary residence of the Emperor of Japan',
                    'category': 'cultural',
                    'gluten_free_info': 'East Gardens area has gluten-free dining options'
                }
            ]
        },
        'Spain': {
            'color': '#C60B1E',
            'flag_emoji': '🇪🇸',
            'dishes': [
                {
                    'name': 'Paella',
                    'local_name': 'Paella',
                    'description': 'Rice dish, usually gluten-free but check seasonings',
                    'ingredients': 'May contain wheat-based seasonings'
                },
                {
                    'name': 'Churros',
                    'local_name': 'Churros',
                    'description': 'Fried dough pastry made with wheat flour',
                    'ingredients': 'Wheat flour, oil, sugar'
                },
                {
                    'name': 'Gazpacho',
                    'local_name': 'Gazpacho',
                    'description': 'Cold soup, usually safe but check for bread thickener',
                    'ingredients': 'Sometimes thickened with bread'
                }
            ],
            'attractions': [
                {
                    'name': 'Sagrada Familia',
                    'local_name': 'Sagrada Família',
                    'description': 'Iconic basilica designed by Antoni Gaudí',
                    'category': 'religious',
                    'gluten_free_info': 'Nearby restaurants in Eixample offer gluten-free menus'
                },
                {
                    'name': 'Alhambra',
                    'local_name': 'Alhambra',
                    'description': 'Moorish palace and fortress complex',
                    'category': 'monument',
                    'gluten_free_info': 'Granada has several dedicated gluten-free bakeries'
                },
                {
                    'name': 'Park Güell',
                    'local_name': 'Park Güell',
                    'description': 'Public park with architectural elements by Gaudí',
                    'category': 'park',
                    'gluten_free_info': 'Café at entrance offers gluten-free snacks'
                }
            ]
        },
        'Mexico': {
            'color': '#006847',
            'flag_emoji': '🇲🇽',
            'dishes': [
                {
                    'name': 'Tortillas',
                    'local_name': 'Tortillas',
                    'description': 'Corn tortillas are safe, wheat tortillas contain gluten',
                    'ingredients': 'Wheat flour (for flour tortillas)'
                },
                {
                    'name': 'Mole',
                    'local_name': 'Mole',
                    'description': 'Complex sauce that may contain wheat flour',
                    'ingredients': 'May contain wheat flour as thickener'
                },
                {
                    'name': 'Tamales',
                    'local_name': 'Tamales',
                    'description': 'Usually made with corn masa, generally safe',
                    'ingredients': 'Corn masa (usually safe)'
                }
            ],
            'attractions': [
                {
                    'name': 'Chichen Itza',
                    'local_name': 'Chichén Itzá',
                    'description': 'Ancient Maya city and archaeological site',
                    'category': 'monument',
                    'gluten_free_info': 'Visitor center restaurant has corn-based options'
                },
                {
                    'name': 'Teotihuacan',
                    'local_name': 'Teotihuacán',
                    'description': 'Ancient Mesoamerican city with pyramids',
                    'category': 'monument',
                    'gluten_free_info': 'Local vendors sell naturally gluten-free corn snacks'
                },
                {
                    'name': 'Frida Kahlo Museum',
                    'local_name': 'Museo Frida Kahlo',
                    'description': 'Museum dedicated to the life and work of Frida Kahlo',
                    'category': 'museum',
                    'gluten_free_info': 'Coyoacán neighborhood has gluten-free restaurants'
                }
            ]
        },
        'United States': {
            'color': '#B22234',
            'flag_emoji': '🇺🇸',
            'dishes': [
                {
                    'name': 'Hamburger',
                    'local_name': 'Hamburger',
                    'description': 'Traditional buns contain wheat',
                    'ingredients': 'Wheat flour bun'
                },
                {
                    'name': 'Fried Chicken',
                    'local_name': 'Fried Chicken',
                    'description': 'Breading typically contains wheat flour',
                    'ingredients': 'Wheat flour breading'
                },
                {
                    'name': 'Apple Pie',
                    'local_name': 'Apple Pie',
                    'description': 'Traditional crust made with wheat flour',
                    'ingredients': 'Wheat flour crust'
                }
            ],
            'attractions': [
                {
                    'name': 'Statue of Liberty',
                    'local_name': 'Statue of Liberty',
                    'description': 'Iconic symbol of freedom and democracy',
                    'category': 'monument',
                    'gluten_free_info': 'Ferry terminal has gluten-free dining options'
                },
                {
                    'name': 'Grand Canyon',
                    'local_name': 'Grand Canyon',
                    'description': 'Massive canyon carved by the Colorado River',
                    'category': 'landmark',
                    'gluten_free_info': 'Visitor centers offer gluten-free snacks'
                },
                {
                    'name': 'Yellowstone National Park',
                    'local_name': 'Yellowstone National Park',
                    'description': 'First national park with geothermal features',
                    'category': 'park',
                    'gluten_free_info': 'Lodge restaurants accommodate gluten-free diets'
                }
            ]
        },
        'Germany': {
            'color': '#FFCE00',
            'flag_emoji': '🇩🇪',
            'dishes': [
                {
                    'name': 'Bratwurst',
                    'local_name': 'Bratwurst',
                    'description': 'Sausage may contain wheat fillers',
                    'ingredients': 'May contain wheat fillers'
                },
                {
                    'name': 'Pretzel',
                    'local_name': 'Brezel',
                    'description': 'Traditional bread made with wheat flour',
                    'ingredients': 'Wheat flour, salt, yeast'
                },
                {
                    'name': 'Schnitzel',
                    'local_name': 'Schnitzel',
                    'description': 'Breaded cutlet with wheat flour coating',
                    'ingredients': 'Wheat flour breading'
                }
            ],
            'attractions': [
                {
                    'name': 'Brandenburg Gate',
                    'local_name': 'Brandenburger Tor',
                    'description': 'Neoclassical monument and symbol of Berlin',
                    'category': 'monument',
                    'gluten_free_info': 'Unter den Linden has several gluten-free restaurants'
                },
                {
                    'name': 'Neuschwanstein Castle',
                    'local_name': 'Schloss Neuschwanstein',
                    'description': 'Fairy-tale castle in Bavaria',
                    'category': 'monument',
                    'gluten_free_info': 'Village below has gluten-free bakery'
                },
                {
                    'name': 'Cologne Cathedral',
                    'local_name': 'Kölner Dom',
                    'description': 'Gothic cathedral and UNESCO World Heritage site',
                    'category': 'religious',
                    'gluten_free_info': 'Cologne city center has many gluten-free options'
                }
            ]
        },
        'United Kingdom': {
            'color': '#012169',
            'flag_emoji': '🇬🇧',
            'dishes': [
                {
                    'name': 'Fish and Chips',
                    'local_name': 'Fish and Chips',
                    'description': 'Batter typically contains wheat flour',
                    'ingredients': 'Wheat flour batter'
                },
                {
                    'name': 'Bangers and Mash',
                    'local_name': 'Bangers and Mash',
                    'description': 'Sausages may contain wheat fillers',
                    'ingredients': 'Sausages may contain wheat'
                },
                {
                    'name': 'Shepherd\'s Pie',
                    'local_name': 'Shepherd\'s Pie',
                    'description': 'May be thickened with wheat flour',
                    'ingredients': 'Often contains wheat flour'
                }
            ],
            'attractions': [
                {
                    'name': 'Big Ben',
                    'local_name': 'Big Ben',
                    'description': 'Iconic clock tower at Westminster',
                    'category': 'landmark',
                    'gluten_free_info': 'Westminster area has excellent gluten-free restaurants'
                },
                {
                    'name': 'Stonehenge',
                    'local_name': 'Stonehenge',
                    'description': 'Prehistoric stone circle monument',
                    'category': 'monument',
                    'gluten_free_info': 'Visitor center café offers gluten-free options'
                },
                {
                    'name': 'Tower of London',
                    'local_name': 'Tower of London',
                    'description': 'Historic castle and former royal residence',
                    'category': 'monument',
                    'gluten_free_info': 'Tower Bridge area has gluten-free dining'
                }
            ]
        },
        'Australia': {
            'color': '#00843D',
            'flag_emoji': '🇦🇺',
            'dishes': [
                {
                    'name': 'Meat Pie',
                    'local_name': 'Meat Pie',
                    'description': 'Traditional pastry with wheat flour crust',
                    'ingredients': 'Wheat flour pastry'
                },
                {
                    'name': 'Lamington',
                    'local_name': 'Lamington',
                    'description': 'Sponge cake made with wheat flour',
                    'ingredients': 'Wheat flour, coconut'
                },
                {
                    'name': 'Vegemite on Toast',
                    'local_name': 'Vegemite on Toast',
                    'description': 'Bread contains wheat',
                    'ingredients': 'Wheat bread'
                }
            ],
            'attractions': [
                {
                    'name': 'Sydney Opera House',
                    'local_name': 'Sydney Opera House',
                    'description': 'Iconic performing arts venue',
                    'category': 'cultural',
                    'gluten_free_info': 'Multiple restaurants with gluten-free menus'
                },
                {
                    'name': 'Uluru',
                    'local_name': 'Uluru',
                    'description': 'Sacred Aboriginal site and monolith',
                    'category': 'landmark',
                    'gluten_free_info': 'Resort dining accommodates gluten-free diets'
                },
                {
                    'name': 'Great Barrier Reef',
                    'local_name': 'Great Barrier Reef',
                    'description': 'World\'s largest coral reef system',
                    'category': 'landmark',
                    'gluten_free_info': 'Tour boats provide gluten-free meal options'
                }
            ]
        },
        'Canada': {
            'color': '#FF0000',
            'flag_emoji': '🇨🇦',
            'dishes': [
                {
                    'name': 'Poutine',
                    'local_name': 'Poutine',
                    'description': 'Gravy may contain wheat flour',
                    'ingredients': 'Gravy often contains wheat flour'
                },
                {
                    'name': 'Tourtière',
                    'local_name': 'Tourtière',
                    'description': 'Meat pie with wheat flour crust',
                    'ingredients': 'Wheat flour pastry'
                },
                {
                    'name': 'Butter Tarts',
                    'local_name': 'Butter Tarts',
                    'description': 'Pastry shells made with wheat flour',
                    'ingredients': 'Wheat flour pastry'
                }
            ],
            'attractions': [
                {
                    'name': 'CN Tower',
                    'local_name': 'CN Tower',
                    'description': 'Iconic telecommunications tower in Toronto',
                    'category': 'landmark',
                    'gluten_free_info': 'Restaurant offers dedicated gluten-free menu'
                },
                {
                    'name': 'Niagara Falls',
                    'local_name': 'Niagara Falls',
                    'description': 'Famous waterfalls on US-Canada border',
                    'category': 'landmark',
                    'gluten_free_info': 'Tourist area has many gluten-free restaurants'
                },
                {
                    'name': 'Banff National Park',
                    'local_name': 'Banff National Park',
                    'description': 'Mountain national park in Alberta',
                    'category': 'park',
                    'gluten_free_info': 'Lodge restaurants accommodate dietary restrictions'
                }
            ]
        },
        'Ireland': {
            'color': '#169B62',
            'flag_emoji': '🇮🇪',
            'dishes': [
                {
                    'name': 'Irish Stew',
                    'local_name': 'Irish Stew',
                    'description': 'May be thickened with wheat flour',
                    'ingredients': 'Sometimes contains wheat flour'
                },
                {
                    'name': 'Soda Bread',
                    'local_name': 'Soda Bread',
                    'description': 'Traditional bread made with wheat flour',
                    'ingredients': 'Wheat flour, buttermilk'
                },
                {
                    'name': 'Guinness',
                    'local_name': 'Guinness',
                    'description': 'Beer made from barley, contains gluten',
                    'ingredients': 'Barley, hops'
                }
            ],
            'attractions': [
                {
                    'name': 'Cliffs of Moher',
                    'local_name': 'Cliffs of Moher',
                    'description': 'Dramatic coastal cliffs on the Atlantic',
                    'category': 'landmark',
                    'gluten_free_info': 'Visitor center café has gluten-free options'
                },
                {
                    'name': 'Trinity College Dublin',
                    'local_name': 'Trinity College Dublin',
                    'description': 'Historic university and home to Book of Kells',
                    'category': 'cultural',
                    'gluten_free_info': 'Dublin has excellent gluten-free restaurants'
                },
                {
                    'name': 'Ring of Kerry',
                    'local_name': 'Ring of Kerry',
                    'description': 'Scenic driving route in County Kerry',
                    'category': 'landmark',
                    'gluten_free_info': 'Many stops along route offer gluten-free meals'
                }
            ]
        }
    }

    # Update countries with complete data
    for country_name, data in countries_data.items():
        try:
            country = Country.objects.get(name=country_name)
            country.color = data['color']
            country.flag_emoji = data['flag_emoji']
            country.save()

            # Add dishes to avoid
            for dish_data in data['dishes']:
                DishesToAvoid.objects.get_or_create(
                    country=country,
                    name=dish_data['name'],
                    defaults={
                        'local_name': dish_data['local_name'],
                        'description': dish_data['description'],
                        'ingredients': dish_data['ingredients']
                    }
                )

            # Add attractions
            for attraction_data in data['attractions']:
                Attraction.objects.get_or_create(
                    country=country,
                    name=attraction_data['name'],
                    defaults={
                        'local_name': attraction_data['local_name'],
                        'description': attraction_data['description'],
                        'category': attraction_data['category'],
                        'gluten_free_info': attraction_data['gluten_free_info']
                    }
                )

        except Country.DoesNotExist:
            continue

class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0006_add_remaining_countries'),
    ]

    operations = [
        migrations.RunPython(add_complete_country_data),
    ]