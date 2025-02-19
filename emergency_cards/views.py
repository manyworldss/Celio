from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import EmergencyCardForm  # Note: Your form should be EmergencyCardForm, not EmergencyCard
from .models import EmergencyCard  # Import the model


@login_required # make sure only logged-in users can access this view
def create_card_or_edit(request):
    try:     # trying to get users existing card
        card = EmergencyCard.objects.get(user=request.user)
            # if card exists, we'll use it to populate the form
    except EmergencyCard.DoesNotExist:
        card = None
    if request.method == 'POST':
        if card:  # if card exists, update it
            form = EmergencyCardForm(request.POST, instance=card)
        else:
            form = EmergencyCardForm(request.POST)
        if form.is_valid():
            card = form.save(commit=False)
            card.user = request.user
            card.save()
            return redirect('emergency_cards:card_detail', card.id)
    else: # GET request
            if card: # if card exists, populate from card
                form = EmergencyCardForm(instance=card)
            else: # if no card, show empty form
                form = EmergencyCardForm()
            return render(request, 'emergency_cards/create_card_or_edit.html', {'form': form,'is_edit': card is not None})







@login_required()
def switch_language(request, card_id):
    card = get_object_or_404(EmergencyCard, id=card_id, user=request.user)
    language = request.GET.get('lang','EN') # default to english if no language specified

    # get message in requested language
    message = card.get_message(language)
    if request.headers.get('HX-Request'): # if it's an HTMX request
        return HttpResponse(message)
    # for regular requests, redirect to card detail
    return redirect("emergency_cards:card_detail", card.id)



@login_required # make sure only logged-in users can access this view
def validate_field(request):
    # get the field name and value from the HTMX POST request
    field_name = request.POST.get('field_name') # 'emergency contact'
    value = request.POST.get('value')
     # creating dictionary with just this single field
    form_data = {field_name: value}
    # creating a form instance with only this fields data
    form = EmergencyCardForm(data=form_data)

    # run validation on the form
    form.is_valid()
    if field_name in form.errors:
        return HttpResponse(
            f'<p class="mt-2 text-sm text-red-600">{form.errors[field_name][0]}</p>'
        )
    return HttpResponse('')


@login_required
def card_detail(request, card_id):
    card = get_object_or_404(EmergencyCard, id=card_id, user=request.user)
    return render(request, 'emergency_cards/card_detail.html', {'card': card})

@login_required
def card_list(request):
    cards = EmergencyCard.objects.filter(user=request.user).order_by('-updated_at')
    return render(request, 'emergency_cards/card_list.html', {'cards': cards})

def home(request):
    return render(request, 'core/home.html')