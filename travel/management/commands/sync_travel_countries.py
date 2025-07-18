from django.core.management.base import BaseCommand
from travel.models import Country
from django.utils.text import slugify

COUNTRY_DATA = [
    {"name": "Spain", "code": "ES", "flag_emoji": "🇪🇸", "language": "Spanish", "language_code": "es", "summary": "Spain has growing celiac awareness with many gluten-free options in cities.", "dining_tips": "Look for 'sin gluten' and ask for gluten-free menus."},
    {"name": "Germany", "code": "DE", "flag_emoji": "🇩🇪", "language": "German", "language_code": "de", "summary": "Germany offers good gluten-free labeling and options in supermarkets.", "dining_tips": "Ask for 'glutenfrei' and check for gluten-free labeling."},
    {"name": "India", "code": "IN", "flag_emoji": "🇮🇳", "language": "Hindi, English", "language_code": "hi", "summary": "India has many naturally gluten-free dishes but cross-contamination is common.", "dining_tips": "Request rice-based dishes and avoid breads."},
    {"name": "South Korea", "code": "KR", "flag_emoji": "🇰🇷", "language": "Korean", "language_code": "ko", "summary": "South Korea has limited celiac awareness; wheat is common in sauces.", "dining_tips": "Ask about wheat in sauces and soups."},
    {"name": "Japan", "code": "JP", "flag_emoji": "🇯🇵", "language": "Japanese", "language_code": "ja", "summary": "Japan has low celiac awareness; soy sauce often contains wheat.", "dining_tips": "Request tamari and avoid breaded/fried foods."},
    {"name": "Saudi Arabia", "code": "SA", "flag_emoji": "🇸🇦", "language": "Arabic", "language_code": "ar", "summary": "Saudi Arabia has limited gluten-free options but growing awareness.", "dining_tips": "Ask for 'bila gluten' and check imported products."},
    {"name": "Russia", "code": "RU", "flag_emoji": "🇷🇺", "language": "Russian", "language_code": "ru", "summary": "Russia has limited celiac awareness; gluten-free products are rare.", "dining_tips": "Bring translation cards and check ingredients."},
    {"name": "United States", "code": "US", "flag_emoji": "🇺🇸", "language": "English", "language_code": "en", "summary": "The US has excellent celiac awareness and gluten-free labeling.", "dining_tips": "Look for certified gluten-free menus."},
    {"name": "Portugal", "code": "PT", "flag_emoji": "🇵🇹", "language": "Portuguese", "language_code": "pt", "summary": "Portugal is improving in celiac awareness, especially in Lisbon and Porto.", "dining_tips": "Ask for 'sem glúten' and check with staff."},
    {"name": "Italy", "code": "IT", "flag_emoji": "🇮🇹", "language": "Italian", "language_code": "it", "summary": "Italy has excellent celiac awareness with many gluten-free options.", "dining_tips": "Look for 'senza glutine' and ask for gluten-free menus."},
    {"name": "China", "code": "CN", "flag_emoji": "🇨🇳", "language": "Chinese", "language_code": "zh", "summary": "China has low celiac awareness; gluten is common in sauces and noodles.", "dining_tips": "Avoid soy sauce and wheat noodles; bring translation cards."},
    {"name": "France", "code": "FR", "flag_emoji": "🇫🇷", "language": "French", "language_code": "fr", "summary": "France is improving in gluten-free awareness, especially in big cities.", "dining_tips": "Look for 'sans gluten' and ask at bakeries and restaurants."}
]

class Command(BaseCommand):
    help = 'Syncs Country table to only contain the specified travel countries.'

    def handle(self, *args, **kwargs):
        allowed_names = [c["name"] for c in COUNTRY_DATA]
        Country.objects.exclude(name__in=allowed_names).delete()
        for data in COUNTRY_DATA:
            obj, created = Country.objects.update_or_create(
                name=data["name"],
                defaults={
                    "slug": slugify(data["name"]),
                    "code": data["code"],
                    "flag_emoji": data["flag_emoji"],
                    "language": data["language"],
                    "language_code": data["language_code"],
                    "summary": data["summary"],
                    "dining_tips": data["dining_tips"]
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Added {data['name']}"))
            else:
                self.stdout.write(self.style.WARNING(f"Updated {data['name']}"))
        self.stdout.write(self.style.SUCCESS("Country table synced."))
