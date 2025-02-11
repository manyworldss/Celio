from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required  # Users must be logged in
from .forms import EmergencyCard

@login_required
def create_card(request):
    if request.method == 'POST':
        form =EmergencyCard(request.POST) # creating form with submitted data
        if form.is_valid():
            card = form.save(commit=False) # creating card but not saving to db yet
            card.user = request.user # attach to current user
            card.save() # now save card
            return redirect("emergency_cards:card_detail", card.id) # redirect to success page
        else:
            form = EmergencyCard() # empty form for GET request
        return render('emergency_cards/create_card.html',{'form': form})

def home(request):
    return render(request, 'core/home.html')

@login_required
def card_detail(request, card_id):
    card = get_object_or_404(EmergencyCard, id=card_id, user=request.user)
    return render(request, 'emergency_cards/card_detail.html', {'card': card})