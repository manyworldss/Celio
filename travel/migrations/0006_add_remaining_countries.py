from django.db import migrations

def add_remaining_countries(apps, schema_editor):
    Country = apps.get_model('travel', 'Country')

    # Add Germany
    Country.objects.get_or_create(
        name="Germany",
        defaults={
            "slug": "germany",
            "code": "DE",
            "flag_emoji": "🇩🇪",
            "language": "German",
            "language_code": "de",
            "celiac_awareness": 4,
            "summary": "Germany has a good understanding of celiac disease, and gluten-free products are widely available.",
            "dining_tips": "Look for 'glutenfrei' on menus. Many health food stores (Reformhaus) stock gluten-free items."
        }
    )

    # Add United Kingdom
    Country.objects.get_or_create(
        name="United Kingdom",
        defaults={
            "slug": "united-kingdom",
            "code": "GB",
            "flag_emoji": "🇬🇧",
            "language": "English",
            "language_code": "en",
            "celiac_awareness": 5,
            "summary": "The UK has excellent celiac awareness, with strict food labeling laws and many gluten-free options.",
            "dining_tips": "Most supermarkets have dedicated gluten-free sections. Restaurants are generally well-informed."
        }
    )

    # Add Australia
    Country.objects.get_or_create(
        name="Australia",
        defaults={
            "slug": "australia",
            "code": "AU",
            "flag_emoji": "🇦🇺",
            "language": "English",
            "language_code": "en",
            "celiac_awareness": 5,
            "summary": "Australia has a very high level of celiac awareness, supported by Coeliac Australia.",
            "dining_tips": "Gluten-free options are common in cafes and restaurants. Look for 'GF' on menus."
        }
    )

    # Add Canada
    Country.objects.get_or_create(
        name="Canada",
        defaults={
            "slug": "canada",
            "code": "CA",
            "flag_emoji": "🇨🇦",
            "language": "English/French",
            "language_code": "en",
            "celiac_awareness": 5,
            "summary": "Canada has strong food labeling regulations and a high level of awareness for celiac disease.",
            "dining_tips": "Many restaurants offer gluten-free menus. Packaged foods are clearly labeled."
        }
    )

    # Add Ireland
    Country.objects.get_or_create(
        name="Ireland",
        defaults={
            "slug": "ireland",
            "code": "IE",
            "flag_emoji": "🇮🇪",
            "language": "English/Irish",
            "language_code": "en",
            "celiac_awareness": 5,
            "summary": "Ireland has a high rate of celiac disease and excellent awareness, supported by the Coeliac Society of Ireland.",
            "dining_tips": "Gluten-free products are widely available. Many pubs and restaurants offer safe options."
        }
    )

class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0005_add_more_countries'),
    ]

    operations = [
        migrations.RunPython(add_remaining_countries),
    ]