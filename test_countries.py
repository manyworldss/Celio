#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'celio.settings')
django.setup()

from travel.models import Country
from travel.views import travel_guide_list
from django.http import HttpRequest

# Test the view directly
from django.test import RequestFactory

factory = RequestFactory()
request = factory.get('/travel/')

# Call the view
response = travel_guide_list(request)

print(f"Response status: {response.status_code}")

# Get the context from the response
if hasattr(response, 'context_data'):
    context = response.context_data
else:
    # For render() responses, we need to access context differently
    context = response.context_data if hasattr(response, 'context_data') else None

if context:
    print(f"Context keys: {list(context.keys())}")
    print(f"Number of travel guides: {len(context['travel_guides'])}")
    
    print("\nCountries in context:")
    for i, country in enumerate(context['travel_guides'], 1):
        print(f"{i}. {country.name} (slug: {country.slug})")
else:
    print("Could not access context data")
    # Let's test the query directly
    from travel.models import Country
    travel_guides = Country.objects.all().order_by('name')
    print(f"Direct query - Number of countries: {travel_guides.count()}")
    
    print("\nCountries from direct query:")
    for i, country in enumerate(travel_guides, 1):
        print(f"{i}. {country.name} (slug: {country.slug})")

print("\nAll countries in database:")
all_countries = Country.objects.all().order_by('name')
for i, country in enumerate(all_countries, 1):
    print(f"{i}. {country.name} (slug: {country.slug})")