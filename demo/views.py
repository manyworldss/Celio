from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.http import JsonResponse
from emergency_cards.models import EmergencyCard
import uuid
from django.utils import timezone
import datetime
from django.views.decorators.http import require_POST

# Create your views here.

def start_demo(request):
    """
    Starts a demo session with a temporary user account and prepopulated data.
    Sets up a guided tour using ShepherdJS.
    """
    # Create a temporary demo user
    demo_username = f"demo_{uuid.uuid4().hex[:8]}"
    demo_email = f"{demo_username}@example.com"
    
    demo_user = User.objects.create_user(
        username=demo_username,
        email=demo_email,
        password=uuid.uuid4().hex,
        first_name="Demo",
        last_name="User",
    )
    
    # Create a sample emergency card
    sample_card = EmergencyCard.objects.create(
        user=demo_user,
        name="Demo Card",
        date_of_birth=timezone.now().date(),
        emergency_contact_name="Emergency Contact",
        emergency_contact_phone="+1234567890",
        preferred_language="EN",
        show_profile_pic=False,
    )
    
    # Add sample translations
    sample_card.translations = {
        "EN": "I have Celiac Disease. I cannot eat anything containing gluten, which is found in wheat, barley, and rye. Cross-contamination is also dangerous for me. Please ensure my food is prepared without any gluten ingredients and on clean surfaces.",
        "ES": "Tengo enfermedad celíaca. No puedo comer nada que contenga gluten, que se encuentra en el trigo, la cebada y el centeno. La contaminación cruzada también es peligrosa para mí. Por favor, asegúrese de que mi comida se prepare sin ingredientes con gluten y en superficies limpias.",
        "FR": "Je souffre de la maladie cœliaque. Je ne peux pas manger d'aliments contenant du gluten, présent dans le blé, l'orge et le seigle. La contamination croisée est également dangereuse pour moi. Veuillez vous assurer que ma nourriture est préparée sans ingrédients contenant du gluten et sur des surfaces propres.",
    }
    sample_card.save()
    
    # Log in as the demo user
    login(request, demo_user)
    
    # Set a session variable to indicate this is a demo session
    request.session['is_demo'] = True
    request.session['demo_start_time'] = timezone.now().isoformat()
    request.session['show_tour'] = True
    
    # Redirect to the card detail page with the tour
    return redirect('emergency_cards:card_detail')


def end_demo(request):
    """
    Ends the demo session, cleaning up the temporary account.
    """
    if request.session.get('is_demo'):
        try:
            # Get the current demo user
            user = request.user
            
            # Delete all their data
            if user.is_authenticated and user.username.startswith('demo_'):
                EmergencyCard.objects.filter(user=user).delete()
                user.delete()
        except Exception as e:
            # Log error but continue
            print(f"Error cleaning up demo: {e}")
        
        # Clear session
        request.session.pop('is_demo', None)
        request.session.pop('demo_start_time', None)
        request.session.pop('show_tour', None)
    
    # Redirect back to home page
    return redirect('home')


@require_POST
def end_tour(request):
    """
    Marks the tour as completed in the session
    """
    if request.session.get('is_demo'):
        request.session['show_tour'] = False
        request.session.modified = True
    
    return JsonResponse({'status': 'success'})
