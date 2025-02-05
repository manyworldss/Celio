from django.shortcuts import render

def home(request):
    features = [
        {
            'name': 'City Safety Map',
            'description': 'Find verified gluten-free restaurants and eateries in your area.',
            'icon': 'icons/map-pin.svg'
        },
        {
            'name': 'Quick Scan',
            'description': 'Instantly check if packaged foods are safe with our barcode scanner.',
            'icon': 'icons/scan.svg'
        },
        {
            'name': 'Rush Hour',
            'description': 'Quick and easy gluten-free recipes for busy city life.',
            'icon': 'icons/clock.svg'
        },
    ]
    return render(request, 'core/home.html', {'features': features})
