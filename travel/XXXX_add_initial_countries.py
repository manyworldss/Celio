# travel/migrations/XXXX_add_initial_countries.py
from django.db import migrations

def add_initial_countries(apps, schema_editor):
    Country = apps.get_model('travel', 'Country')
    RestaurantPhrase = apps.get_model('travel', 'RestaurantPhrase')
    DishesToAvoid = apps.get_model('travel', 'DishesToAvoid')
    
    # Add some initial countries
    italy = Country.objects.create(
        name="Italy",
        code="IT",
        flag_emoji="🇮🇹",
        language="Italian",
        language_code="it",
        celiac_awareness=4,
        summary="Italy has one of the highest rates of celiac disease in the world, making it surprisingly celiac-friendly. The Italian Celiac Association (AIC) works with restaurants to certify them as safe for celiacs.",
        dining_tips="Look for restaurants with the AIC certification logo. Many Italian restaurants offer gluten-free pasta and pizza options. Always specify 'Sono celiaco/a' (I am celiac) rather than just asking for gluten-free."
    )
    
    japan = Country.objects.create(
        name="Japan",
        code="JP",
        flag_emoji="🇯🇵",
        language="Japanese",
        language_code="ja",
        celiac_awareness=2,
        summary="Celiac awareness in Japan is relatively low. Soy sauce, which contains wheat, is used in many dishes. Language barriers can make communication challenging.",
        dining_tips="Carry a detailed Japanese translation card. Consider staying in accommodations with kitchen access. Research restaurants in advance and look for larger cities with international restaurants that may be more familiar with dietary restrictions."
    )
    
    france = Country.objects.create(
        name="France",
        code="FR",
        flag_emoji="🇫🇷",
        language="French",
        language_code="fr",
        celiac_awareness=3,
        summary="France has improved its celiac awareness in recent years. The AFDIAG (French Association of Gluten Intolerant People) provides resources for those with celiac disease.",
        dining_tips="Look for restaurants with 'sans gluten' options. Be cautious with sauces and soups which often contain flour. Consider explaining your needs in advance for a better dining experience."
    )
    
    # Add some restaurant phrases
    # Italy
    RestaurantPhrase.objects.create(
        country=italy,
        english_text="I have celiac disease. I cannot eat gluten, which is found in wheat, barley, and rye.",
        translated_text="Sono celiaco/a. Non posso mangiare glutine, che si trova nel grano, nell'orzo e nella segale.",
        category="general"
    )
    
    RestaurantPhrase.objects.create(
        country=italy,
        english_text="Is this dish gluten-free?",
        translated_text="Questo piatto è senza glutine?",
        category="ordering"
    )
    
    # Japan
    RestaurantPhrase.objects.create(
        country=japan,
        english_text="I have celiac disease. I cannot eat gluten, which is found in wheat, barley, and rye.",
        translated_text="私はセリアック病です。小麦、大麦、ライ麦に含まれるグルテンを食べることができません。",
        pronunciation="Watashi wa seriakku byō desu. Komugi, ōmugi, raimugi ni fukumareru guruten o taberu koto ga dekimasen.",
        category="general"
    )
    
    RestaurantPhrase.objects.create(
        country=japan,
        english_text="Does this contain soy sauce?",
        translated_text="これは醤油が含まれていますか？",
        pronunciation="Kore wa shōyu ga fukumarete imasu ka?",
        category="ingredients"
    )
    
    # France
    RestaurantPhrase.objects.create(
        country=france,
        english_text="I have celiac disease. I cannot eat gluten, which is found in wheat, barley, and rye.",
        translated_text="Je suis atteint(e) de maladie cœliaque. Je ne peux pas manger de gluten, que l'on trouve dans le blé, l'orge et le seigle.",
        category="general"
    )
    
    RestaurantPhrase.objects.create(
        country=france,
        english_text="Is this dish gluten-free?",
        translated_text="Est-ce que ce plat est sans gluten?",
        category="ordering"
    )
    
    # Add dishes to avoid
    # Italy
    DishesToAvoid.objects.create(
        country=italy,
        name="Regular Pasta",
        local_name="Pasta",
        description="Traditional Italian pasta made from wheat flour",
        ingredients="Wheat flour, sometimes eggs"
    )
    
    DishesToAvoid.objects.create(
        country=italy,
        name="Regular Pizza",
        local_name="Pizza",
        description="Traditional Italian pizza with wheat-based crust",
        ingredients="Wheat flour, yeast"
    )
    
    # Japan
    DishesToAvoid.objects.create(
        country=japan,
        name="Ramen",
        local_name="ラーメン",
        description="Japanese noodle soup with wheat-based noodles",
        ingredients="Wheat flour noodles, often soy sauce in broth"
    )
    
    DishesToAvoid.objects.create(
        country=japan,
        name="Tempura",
        local_name="天ぷら",
        description="Battered and deep-fried seafood or vegetables",
        ingredients="Wheat flour batter"
    )
    
    # France
    DishesToAvoid.objects.create(
        country=france,
        name="Croissant",
        local_name="Croissant",
        description="Flaky, buttery pastry",
        ingredients="Wheat flour, butter, yeast"
    )
    
    DishesToAvoid.objects.create(
        country=france,
        name="Baguette",
        local_name="Baguette",
        description="Traditional French bread",
        ingredients="Wheat flour, yeast, salt"
    )

def remove_data(apps, schema_editor):
    Country = apps.get_model('travel', 'Country')
    Country.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_initial_countries, remove_data),
    ]