from django.shortcuts import render

# Create your views here.
# travel/views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Country, DishesToAvoid, RestaurantPhrase

@login_required
def travel_guide_list(request):
    """View for listing available country guides"""
    countries = Country.objects.all().order_by('name')
    
    # Get premium status - for now just a placeholder
    is_premium = False  # This would be determined from user's subscription status
    
    return render(request, 'travel/travel_guide_list.html', {
        'countries': countries,
        'is_premium': is_premium
    })

@login_required
def country_detail(request, country_code):
    """View for detailed country guide"""
    country = get_object_or_404(Country, code=country_code.upper())
    
    # Get dishes to avoid
    dishes_to_avoid = DishesToAvoid.objects.filter(country=country)
    
    # Get restaurant phrases by category
    general_phrases = RestaurantPhrase.objects.filter(country=country, category='general')
    ordering_phrases = RestaurantPhrase.objects.filter(country=country, category='ordering')
    ingredient_phrases = RestaurantPhrase.objects.filter(country=country, category='ingredients')
    emergency_phrases = RestaurantPhrase.objects.filter(country=country, category='emergency')
    
    # Get premium status - for now just a placeholder
    is_premium = False  # This would be determined from user's subscription status
    
    return render(request, 'travel/country_detail.html', {
        'country': country,
        'dishes_to_avoid': dishes_to_avoid,
        'general_phrases': general_phrases,
        'ordering_phrases': ordering_phrases,
        'ingredient_phrases': ingredient_phrases,
        'emergency_phrases': emergency_phrases,
        'is_premium': is_premium
    })

@login_required
def restaurant_card(request, country_code):
    """View for printable restaurant card"""
    country = get_object_or_404(Country, code=country_code.upper())
    
    # Get key phrases for the restaurant card
    general_phrases = RestaurantPhrase.objects.filter(country=country, category='general')
    ordering_phrases = RestaurantPhrase.objects.filter(country=country, category='ordering')
    ingredient_phrases = RestaurantPhrase.objects.filter(country=country, category='ingredients')
    
    # Get premium status - for now just a placeholder
    is_premium = False  # This would be determined from user's subscription status
    
    if not is_premium:
        # Redirect non-premium users to upgrade page
        return redirect('subscription:upgrade')
    
    return render(request, 'travel/restaurant_card.html', {
        'country': country,
        'general_phrases': general_phrases,
        'ordering_phrases': ordering_phrases,
        'ingredient_phrases': ingredient_phrases,
    })