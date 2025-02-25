import os
import sys

# Add project directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'celio.settings')
import django
django.setup()

from django.contrib.auth.models import User
from emergency_cards.models import EmergencyCard

def cleanup_cards():
    print("Starting cleanup process...")
    for user in User.objects.all():
        cards = EmergencyCard.objects.filter(user=user).order_by('-updated_at')
        if cards.count() > 1:
            print(f"User {user.username} has {cards.count()} cards. Keeping most recent.")
            # Keep only the first (most recent) card
            for card in cards[1:]:
                print(f"Deleting card {card.id}")
                card.delete()
    print("Cleanup complete!")

if __name__ == "__main__":
    import django
    django.setup()
    cleanup_cards()