from django.core.management.base import BaseCommand
from travel.models import Country, Attraction

class Command(BaseCommand):
    help = 'Populate attractions data for countries'

    def handle(self, *args, **options):
        self.stdout.write('Populating attractions data...')
        
        attractions_data = {
            'Italy': [
                {
                    'name': 'Colosseum',
                    'local_name': 'Colosseo',
                    'description': 'Ancient Roman amphitheater and iconic symbol of Imperial Rome. One of the New Seven Wonders of the World.',
                    'category': 'monument',
                    'gluten_free_info': 'Nearby restaurants like Flavio al Velavevodetto offer excellent gluten-free Roman cuisine.'
                },
                {
                    'name': 'Vatican Museums',
                    'local_name': 'Musei Vaticani',
                    'description': 'World-renowned art collection including the Sistine Chapel with Michelangelo\'s masterpieces.',
                    'category': 'museum',
                    'gluten_free_info': 'The museum cafeteria offers gluten-free options, and nearby Via Cola di Rienzo has several celiac-friendly restaurants.'
                },
                {
                    'name': 'Trevi Fountain',
                    'local_name': 'Fontana di Trevi',
                    'description': 'Baroque fountain and one of the most famous fountains in the world. Tradition says throwing a coin ensures return to Rome.',
                    'category': 'landmark',
                    'gluten_free_info': 'Nearby Ginger restaurant specializes in gluten-free Italian cuisine.'
                }
            ],
            'France': [
                {
                    'name': 'Eiffel Tower',
                    'local_name': 'Tour Eiffel',
                    'description': 'Iron lattice tower and global cultural icon of France, offering spectacular views of Paris.',
                    'category': 'landmark',
                    'gluten_free_info': 'The tower\'s restaurants offer gluten-free options, and nearby Chambelland bakery serves excellent gluten-free pastries.'
                },
                {
                    'name': 'Louvre Museum',
                    'local_name': 'Musée du Louvre',
                    'description': 'World\'s largest art museum, home to the Mona Lisa and thousands of other masterpieces.',
                    'category': 'museum',
                    'gluten_free_info': 'Museum restaurants have gluten-free options, and nearby Noglu restaurant specializes in gluten-free French cuisine.'
                },
                {
                    'name': 'Notre-Dame Cathedral',
                    'local_name': 'Cathédrale Notre-Dame',
                    'description': 'Medieval Catholic cathedral, masterpiece of French Gothic architecture.',
                    'category': 'religious',
                    'gluten_free_info': 'Île Saint-Louis nearby has several restaurants with gluten-free options including Berthillon ice cream.'
                }
            ],
            'Spain': [
                {
                    'name': 'Sagrada Familia',
                    'local_name': 'Basílica de la Sagrada Família',
                    'description': 'Unfinished basilica designed by Antoni Gaudí, UNESCO World Heritage Site.',
                    'category': 'religious',
                    'gluten_free_info': 'Barcelona has excellent gluten-free options nearby including Sants restaurant and gluten-free bakeries.'
                },
                {
                    'name': 'Alhambra',
                    'local_name': 'La Alhambra',
                    'description': 'Palace and fortress complex showcasing Islamic architecture in Granada.',
                    'category': 'monument',
                    'gluten_free_info': 'Granada offers traditional gluten-free tapas at restaurants like Bodegas Castañeda.'
                },
                {
                    'name': 'Park Güell',
                    'local_name': 'Parc Güell',
                    'description': 'Public park with architectural elements designed by Antoni Gaudí.',
                    'category': 'park',
                    'gluten_free_info': 'Nearby Gràcia neighborhood has several celiac-friendly restaurants and cafes.'
                }
            ],
            'United States': [
                {
                    'name': 'Statue of Liberty',
                    'local_name': 'Statue of Liberty',
                    'description': 'Neoclassical sculpture and symbol of freedom and democracy.',
                    'category': 'monument',
                    'gluten_free_info': 'Ferry services offer gluten-free snacks, and NYC has numerous gluten-free restaurants.'
                },
                {
                    'name': 'Grand Canyon',
                    'local_name': 'Grand Canyon',
                    'description': 'Steep-sided canyon carved by the Colorado River, one of the most visited national parks.',
                    'category': 'landmark',
                    'gluten_free_info': 'Visitor centers have gluten-free snacks, and nearby Flagstaff has several celiac-friendly restaurants.'
                },
                {
                    'name': 'Smithsonian Museums',
                    'local_name': 'Smithsonian Institution',
                    'description': 'World\'s largest museum complex with 19 museums and galleries.',
                    'category': 'museum',
                    'gluten_free_info': 'Museum cafeterias offer gluten-free options, and DC has many dedicated gluten-free restaurants.'
                }
            ],
            'Japan': [
                {
                    'name': 'Mount Fuji',
                    'local_name': '富士山 (Fujisan)',
                    'description': 'Sacred mountain and highest peak in Japan, UNESCO World Heritage Site.',
                    'category': 'landmark',
                    'gluten_free_info': 'Nearby areas offer rice-based dishes and dedicated gluten-free restaurants in Kawaguchi-ko.'
                },
                {
                    'name': 'Senso-ji Temple',
                    'local_name': '浅草寺 (Sensō-ji)',
                    'description': 'Ancient Buddhist temple in Tokyo, the city\'s oldest temple.',
                    'category': 'religious',
                    'gluten_free_info': 'Asakusa area has traditional rice crackers and several restaurants with gluten-free sushi options.'
                },
                {
                    'name': 'Fushimi Inari Shrine',
                    'local_name': '伏見稲荷大社',
                    'description': 'Shinto shrine famous for thousands of vermillion torii gates.',
                    'category': 'religious',
                    'gluten_free_info': 'Kyoto offers traditional kaiseki cuisine with rice-based dishes and dedicated gluten-free restaurants.'
                }
            ],
            'South Korea': [
                {
                    'name': 'Gyeongbokgung Palace',
                    'local_name': '경복궁',
                    'description': 'Main royal palace of the Joseon dynasty, built in 1395.',
                    'category': 'monument',
                    'gluten_free_info': 'Nearby Insadong area has traditional tea houses and restaurants offering rice-based Korean dishes.'
                },
                {
                    'name': 'Jeju Island',
                    'local_name': '제주도',
                    'description': 'Volcanic island known for its natural beauty and unique culture.',
                    'category': 'landmark',
                    'gluten_free_info': 'Island specializes in fresh seafood and rice dishes, with several gluten-free friendly restaurants.'
                },
                {
                    'name': 'Bukchon Hanok Village',
                    'local_name': '북촌한옥마을',
                    'description': 'Traditional Korean village with hundreds of traditional houses.',
                    'category': 'cultural',
                    'gluten_free_info': 'Area offers traditional Korean rice cakes and tea houses with gluten-free options.'
                }
            ],
            'Saudi Arabia': [
                {
                    'name': 'Masjid al-Haram',
                    'local_name': 'المسجد الحرام',
                    'description': 'Holiest mosque in Islam, surrounding the Kaaba in Mecca.',
                    'category': 'religious',
                    'gluten_free_info': 'Mecca offers rice-based Middle Eastern dishes and hotels with gluten-free dining options.'
                },
                {
                    'name': 'Al-Masjid an-Nabawi',
                    'local_name': 'المسجد النبوي',
                    'description': 'Second holiest mosque in Islam, located in Medina.',
                    'category': 'religious',
                    'gluten_free_info': 'Medina has traditional rice dishes and dates, with hotels offering gluten-free meal options.'
                },
                {
                    'name': 'Edge of the World',
                    'local_name': 'جبل فهرين',
                    'description': 'Dramatic cliff formation offering spectacular desert views near Riyadh.',
                    'category': 'landmark',
                    'gluten_free_info': 'Riyadh has international restaurants with gluten-free options and traditional rice-based Saudi cuisine.'
                }
            ],
            'Russia': [
                {
                    'name': 'Red Square',
                    'local_name': 'Красная площадь',
                    'description': 'Historic square in Moscow, home to the Kremlin and St. Basil\'s Cathedral.',
                    'category': 'landmark',
                    'gluten_free_info': 'Moscow has several gluten-free restaurants and traditional buckwheat dishes.'
                },
                {
                    'name': 'Hermitage Museum',
                    'local_name': 'Эрмитаж',
                    'description': 'One of the world\'s largest and oldest museums in St. Petersburg.',
                    'category': 'museum',
                    'gluten_free_info': 'St. Petersburg offers gluten-free Russian cuisine and international restaurants with celiac options.'
                },
                {
                    'name': 'Trans-Siberian Railway',
                    'local_name': 'Транссибирская магистраль',
                    'description': 'Network of railways connecting Moscow with the Far East.',
                    'category': 'landmark',
                    'gluten_free_info': 'Train dining cars can accommodate gluten-free requests, and major stops have restaurants with options.'
                }
            ],
            'India': [
                {
                    'name': 'Taj Mahal',
                    'local_name': 'ताज महल',
                    'description': 'Ivory-white marble mausoleum and UNESCO World Heritage Site in Agra.',
                    'category': 'monument',
                    'gluten_free_info': 'Agra offers rice-based Indian dishes and several restaurants with gluten-free options.'
                },
                {
                    'name': 'Red Fort',
                    'local_name': 'लाल किला',
                    'description': 'Historic fortified palace in Delhi, symbol of Mughal power.',
                    'category': 'monument',
                    'gluten_free_info': 'Delhi has numerous restaurants offering gluten-free Indian cuisine and rice-based dishes.'
                },
                {
                    'name': 'Gateway of India',
                    'local_name': 'भारत का प्रवेशद्वार',
                    'description': 'Arch monument built during the British Raj in Mumbai.',
                    'category': 'monument',
                    'gluten_free_info': 'Mumbai offers excellent South Indian rice dishes and restaurants with dedicated gluten-free menus.'
                }
            ],
            'Australia': [
                {
                    'name': 'Sydney Opera House',
                    'local_name': 'Sydney Opera House',
                    'description': 'Multi-venue performing arts center and UNESCO World Heritage Site, iconic symbol of Australia.',
                    'category': 'landmark',
                    'gluten_free_info': 'The Opera House restaurants offer gluten-free options, and Sydney has numerous celiac-friendly dining establishments.'
                },
                {
                    'name': 'Uluru',
                    'local_name': 'Ayers Rock',
                    'description': 'Large sandstone rock formation sacred to Aboriginal Australians, located in Uluru-Kata Tjuta National Park.',
                    'category': 'landmark',
                    'gluten_free_info': 'Resort dining offers gluten-free options, and Alice Springs has several restaurants catering to celiac needs.'
                },
                {
                    'name': 'Great Barrier Reef',
                    'local_name': 'Great Barrier Reef',
                    'description': 'World\'s largest coral reef system and UNESCO World Heritage Site, visible from outer space.',
                    'category': 'landmark',
                    'gluten_free_info': 'Cairns and Port Douglas offer excellent gluten-free seafood restaurants and tour operators provide celiac-safe meals.'
                },
                {
                    'name': 'Royal Botanic Gardens',
                    'local_name': 'Royal Botanic Gardens Sydney',
                    'description': 'Historic botanical garden in Sydney with stunning harbor views and diverse plant collections.',
                    'category': 'park',
                    'gluten_free_info': 'Garden cafe offers gluten-free options, and nearby Circular Quay has many celiac-friendly restaurants.'
                }
            ]
        }
        
        for country_name, attractions in attractions_data.items():
            try:
                country = Country.objects.get(name=country_name)
                self.stdout.write(f'Adding attractions for {country_name}...')
                
                for attraction_data in attractions:
                    attraction, created = Attraction.objects.get_or_create(
                        country=country,
                        name=attraction_data['name'],
                        defaults={
                            'local_name': attraction_data['local_name'],
                            'description': attraction_data['description'],
                            'category': attraction_data['category'],
                            'gluten_free_info': attraction_data['gluten_free_info']
                        }
                    )
                    
                    if created:
                        self.stdout.write(f'  ✓ Added {attraction.name}')
                    else:
                        self.stdout.write(f'  - {attraction.name} already exists')
                        
            except Country.DoesNotExist:
                self.stdout.write(f'Country {country_name} not found, skipping...')
        
        self.stdout.write(self.style.SUCCESS('Successfully populated attractions data!'))