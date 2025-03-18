from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST

@login_required
def start_tour(request):
    """Show the tour page"""
    return render(request, 'onboarding/tour.html')

@login_required
@require_POST
def complete_tour(request):
    """Mark the tour as completed"""
    request.user.onboarding_status.has_completed_tour = True
    request.user.onboarding_status.save()
    return JsonResponse({'status': 'success'})

@login_required
def show_tour_prompt(request):
    """Check if user needs tour and show prompt"""
    show_prompt = not request.user.onboarding_status.has_completed_tour
    return render(request, 'onboarding/tour_prompt.html', {'show_prompt': show_prompt})
# Create your views here.
