from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Country, DishesToAvoid, RestaurantPhrase

def travel_guide_list(request):
    """View for listing available country guides"""
    travel_guides = Country.objects.all().order_by('name')
    
    return render(request, 'travel/travel_guide_list.html', {
        'travel_guides': travel_guides
    })

def country_detail(request, slug):
    """View for detailed country guide"""
    country = get_object_or_404(Country, slug=slug)
    
    # Get dishes to avoid
    dishes_to_avoid = DishesToAvoid.objects.filter(country=country)
    
    # Get restaurant phrases by category
    general_phrases = RestaurantPhrase.objects.filter(country=country, category='general')
    ordering_phrases = RestaurantPhrase.objects.filter(country=country, category='ordering')
    ingredient_phrases = RestaurantPhrase.objects.filter(country=country, category='ingredients')
    e_card_phrases = RestaurantPhrase.objects.filter(country=country, category='message')
    
    return render(request, 'travel/country_detail.html', {
        'country': country,
        'dishes_to_avoid': dishes_to_avoid,
        'general_phrases': general_phrases,
        'ordering_phrases': ordering_phrases,
        'ingredient_phrases': ingredient_phrases,
        'e_card_phrases': e_card_phrases
    })

def restaurant_card(request, slug):
    """View for printable restaurant card"""
    country = get_object_or_404(Country, slug=slug)
    
    # Get key phrases for the restaurant card
    general_phrases = RestaurantPhrase.objects.filter(country=country, category='general')
    ordering_phrases = RestaurantPhrase.objects.filter(country=country, category='ordering')
    ingredient_phrases = RestaurantPhrase.objects.filter(country=country, category='ingredients')
    
    return render(request, 'travel/restaurant_card.html', {
        'country': country,
        'general_phrases': general_phrases,
        'ordering_phrases': ordering_phrases,
        'ingredient_phrases': ingredient_phrases,
    })