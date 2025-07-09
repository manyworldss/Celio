from django.db import migrations

def remove_countries(apps, schema_editor):
    Country = apps.get_model('travel', 'Country')
    Country.objects.filter(code__in=['ES', 'MX', 'US']).delete()

def add_more_countries(apps, schema_editor):
    Country = apps.get_model('travel', 'Country')

    # Add Spain
    Country.objects.get_or_create(
        name="Spain",
        defaults={
            "slug": "spain",
            "code": "ES",
            "flag_emoji": "🇪🇸",
            "language": "Spanish",
            "language_code": "es",
            "celiac_awareness": 4,
            "summary": "Spain is very celiac-friendly, with high awareness and many gluten-free options available.",
            "dining_tips": "Look for 'sin gluten' on menus. Many restaurants are knowledgeable about celiac disease."
        }
    )

    # Add Mexico
    Country.objects.get_or_create(
        name="Mexico",
        defaults={
            "slug": "mexico",
            "code": "MX",
            "flag_emoji": "🇲🇽",
            "language": "Spanish",
            "language_code": "es",
            "celiac_awareness": 3,
            "summary": "Corn is a staple in Mexican cuisine, but cross-contamination can be a risk. Awareness is growing.",
            "dining_tips": "Confirm that corn tortillas are 100% corn. Be cautious with moles and sauces."
        }
    )

    # Add USA
    Country.objects.get_or_create(
        name="USA",
        defaults={
            "slug": "usa",
            "code": "US",
            "flag_emoji": "🇺🇸",
            "language": "English",
            "language_code": "en",
            "celiac_awareness": 5,
            "summary": "The USA has high awareness of celiac disease, with extensive gluten-free products and labeling laws.",
            "dining_tips": "Most restaurants offer gluten-free menus. Always inform your server of your dietary needs."
        }
    )

class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0004_attraction'),
    ]

    operations = [
        migrations.RunPython(remove_countries),
        migrations.RunPython(add_more_countries),
    ]