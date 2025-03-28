import io
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .models import EmergencyCard
from .forms import EmergencyCardForm
import qrcode
import base64
# For PDF generation
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle



@login_required
def switch_language(request):
    # get the card
    card = get_object_or_404(EmergencyCard, user=request.user)
    language = request.GET.get('lang', 'EN')  # default to english if no language specified
    
    # Case insensitive comparison for language codes
    upper_lang = language.upper()
    
    # Get all available language keys in uppercase for comparison
    available_langs = {lang.upper(): lang for lang in card.translations.keys()}
    
    # Make sure requested language exists in translations
    if upper_lang in available_langs:
        language = available_langs[upper_lang]  # Use original case from card
    elif card.translations:
        language = next(iter(card.translations.keys()))
    
    # get message in requested language
    message = card.get_message(language)
    
    # Get language display name
    current_lang_display = dict(EmergencyCard.LANGUAGE_CHOICES).get(language.lower(), language)
    
    # Create languages dictionary for the template
    languages = {}
    for lang_code in card.translations.keys():
        lang_name = dict(EmergencyCard.LANGUAGE_CHOICES).get(lang_code.lower(), lang_code)
        languages[lang_code] = lang_name
    
    if request.headers.get('HX-Request'):  # if it's an HTMX request
        # return formatted message content
        return render(request, 'emergency_cards/partials/message_content.html', {
            'message': message,
            'card': card, 
            'current_lang': language,
            'current_lang_display': current_lang_display,
            'languages': languages,
            'theme': card.theme
        })
    
    # for regular requests, redirect to card detail with language parameter
    return redirect(reverse('emergency_cards:card_detail') + f"?lang={language}")


@login_required # make sure only logged-in users can access this view
def create_card_or_edit(request):
    try:     # trying to get users existing card
        card = EmergencyCard.objects.get(user=request.user)
            # if card exists, we'll use it to populate the form
    except EmergencyCard.DoesNotExist:
        card = None
    
    # Get the currently active language from the form
    active_language = request.POST.get('active_language', 'en').upper()
    
    if request.method == 'POST':
        if card:  # if card exists, update it
            form = EmergencyCardForm(request.POST, request.FILES, instance=card)
        else:
            form = EmergencyCardForm(request.POST, request.FILES)
        
        if form.is_valid():
            card = form.save(commit=False)
            card.user = request.user
            
            # Get the message from the textarea
            card_message = request.POST.get('card_message', '')
            
            # Initialize translations if needed
            if not card.translations:
                card.translations = {}
            
            # Update the message for the active language
            if active_language and card_message:
                card.translations[active_language] = card_message
            
            # Make sure at least one language translation exists (English)
            if not card.translations or 'EN' not in card.translations:
                if 'message_en' in form.cleaned_data and form.cleaned_data['message_en']:
                    card.translations['EN'] = form.cleaned_data['message_en']
                else:
                    card.translations['EN'] = "I have celiac disease/gluten sensitivity and cannot consume any foods containing gluten."
            
            # Set preferred language if not already set
            if not card.preferred_language and card.translations:
                card.preferred_language = active_language
            
            card.save()
            messages.success(request, "Emergency card successfully updated!" if card else "Emergency card successfully created!")
            return redirect('emergency_cards:card_detail')
        else:
            # Return the form with errors if not valid
            messages.error(request, "Please correct the errors below.")
            return render(request, 'emergency_cards/create_card_or_edit.html', {'form': form, 'is_edit': card is not None})
    else: # GET request
        if card: # if card exists, populate from card
            form = EmergencyCardForm(instance=card)
        else: # if no card, show empty form
            form = EmergencyCardForm()
        return render(request, 'emergency_cards/create_card_or_edit.html', {'form': form,'is_edit': card is not None})


@login_required
def delete_card(request):
    card = get_object_or_404(EmergencyCard, user=request.user)

    if request.method == 'POST':
        card.delete()
        return redirect('core:home') # redirect home after deletion
    return render(request, 'emergency_cards/delete_card.html', {'card': card})



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
def card_detail(request):
    try:
        card = EmergencyCard.objects.get(user=request.user)
        # Get the current language from query parameter, preferred language, or default to English
        current_lang = request.GET.get('lang')
        
        if not current_lang:
            # Use preferred language if available, otherwise default to English
            current_lang = card.preferred_language if hasattr(card, 'preferred_language') and card.preferred_language else 'EN'
        
        # Make sure the language exists in translations, otherwise default to English
        if current_lang.upper() not in card.translations:
            if 'EN' in card.translations:
                current_lang = 'EN'
            elif card.translations:  # If there are translations but not the one we want
                current_lang = next(iter(card.translations.keys()))  # Get the first available language
            else:
                # No translations available
                return redirect('emergency_cards:create_card')
        
        # Get the language display name for the current language
        current_lang_display = dict(EmergencyCard.LANGUAGE_CHOICES).get(current_lang.lower(), current_lang)
        
        # Create languages dictionary for the template
        languages = {}
        for lang_code in card.translations.keys():
            lang_name = dict(EmergencyCard.LANGUAGE_CHOICES).get(lang_code.lower(), lang_code)
            languages[lang_code] = lang_name
        
        context = {
            'card': card,
            'current_lang': current_lang,
            'current_lang_display': current_lang_display,
            'message': card.get_message(current_lang),
            'languages': languages,
            'is_premium': getattr(request, 'is_premium', True),  # Always allow access in demo mode
            'is_demo': request.session.get('is_demo', False),
        }
        return render(request, 'emergency_cards/card_detail.html', context)
    except EmergencyCard.DoesNotExist:
        # Redirect to create card page with a helpful message
        messages.info(request, "You don't have an emergency card yet. Let's create one!")
        return redirect('emergency_cards:create_card')


@login_required
def preview_card(request):
    card = get_object_or_404(EmergencyCard, user=request.user)
    language = request.GET.get('lang', 'EN')  # Get preferred language

    return render(request, 'emergency_cards/preview_card.html', {
        'card': card,
        'current_language': language
    })


@login_required
def download_card(request):
    card = get_object_or_404(EmergencyCard, user=request.user)
    format_type = request.GET.get('format', 'pdf')
    language = request.GET.get('lang', card.preferred_language)
    
    # For wallet cards, will implement this later
    if format_type == 'wallet':
        # Placeholder for wallet card functionality
        return render(request, 'emergency_cards/download.html', {
            'card': card,
            'error': 'Wallet card format is coming soon!'
        })
    
    # For showing the modal via HTMX
    if request.headers.get('HX-Request') and not request.GET.get('download', ''):
        return render(request, 'emergency_cards/download.html', {'card': card})
    
    # Get page size
    page_size_param = request.GET.get('size', 'letter')
    page_size = letter if page_size_param == 'letter' else A4
    
    # Create a file-like buffer to receive PDF data
    buffer = io.BytesIO()
    
    # Create the PDF document using ReportLab
    doc = SimpleDocTemplate(
        buffer,
        pagesize=page_size,
        rightMargin=0.5*inch,
        leftMargin=0.5*inch,
        topMargin=0.5*inch,
        bottomMargin=0.5*inch
    )
    
    # Get card message in the requested language
    message = card.get_message(language)
    
    # Define styles
    styles = getSampleStyleSheet()
    
    # Define custom theme-based styles
    if card.theme == 'modern':
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Title'],
            textColor=colors.white,
            backColor=colors.purple
        )
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            textColor=colors.white
        )
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            textColor=colors.white
        )
        contact_style = ParagraphStyle(
            'ContactStyle',
            parent=styles['Normal'],
            backColor=colors.Color(1, 1, 1, 0.1),
            textColor=colors.white,
            spaceBefore=10,
            spaceAfter=10,
            borderPadding=10
        )
        bg_color = colors.purple
    elif card.theme == 'minimal':
        title_style = styles['Title']
        heading_style = styles['Heading2']
        normal_style = styles['Normal']
        contact_style = ParagraphStyle(
            'ContactStyle',
            parent=styles['Normal'],
            backColor=colors.lightgrey,
            spaceBefore=10,
            spaceAfter=10,
            borderPadding=10
        )
        bg_color = colors.white
    else:  # Classic theme
        title_style = styles['Title']
        heading_style = styles['Heading2']
        normal_style = styles['Normal']
        contact_style = ParagraphStyle(
            'ContactStyle',
            parent=styles['Normal'],
            backColor=colors.lightgrey,
            spaceBefore=10,
            spaceAfter=10,
            borderPadding=10
        )
        bg_color = colors.white
    
    # Define badge style based on condition
    if card.condition == 'CEL':
        condition_color = colors.red
    elif card.condition == 'SEN':
        condition_color = colors.orange
    else:
        condition_color = colors.brown
    
    # Create the content for the PDF
    content = []
    
    # Add condition badge
    condition_text = card.get_condition_display()
    condition_para = Paragraph(
        f"<para backColor='{condition_color}' textColor='white' borderPadding='5'>{condition_text}</para>",
        styles['Normal']
    )
    content.append(condition_para)
    content.append(Spacer(1, 0.2*inch))
    
    # Add title
    content.append(Paragraph("Emergency Medical Card", title_style))
    content.append(Spacer(1, 0.2*inch))
    
    # Add medical information
    content.append(Paragraph("Medical Information", heading_style))
    content.append(Spacer(1, 0.1*inch))
    
    # Process message text (replace newlines with paragraph breaks)
    for paragraph in message.split('\n'):
        if paragraph.strip():
            content.append(Paragraph(paragraph, normal_style))
            content.append(Spacer(1, 0.1*inch))
    
    # Add emergency contact information
    content.append(Paragraph("Emergency Contact", heading_style))
    content.append(Spacer(1, 0.1*inch))
    
    # Create a table for contact info
    contact_data = [
        ['Name:', card.emergency_contact_name],
        ['Relationship:', card.emergency_contact_relationship],
        ['Phone:', card.emergency_contact_phone]
    ]
    
    contact_table = Table(contact_data, colWidths=[1.5*inch, 4*inch])
    contact_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey if card.theme != 'modern' else colors.Color(1, 1, 1, 0.1)),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black if card.theme != 'modern' else colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    
    content.append(contact_table)
    content.append(Spacer(1, 0.2*inch))
    
    # Add footer
    footer_text = f"Generated by Celio Emergency Card System on {timezone.now().strftime('%B %d, %Y')} | Language: {language}"
    content.append(Paragraph(footer_text, styles['Italic']))
    
    # Build the PDF
    doc.build(content)
    
    # Get the value of the BytesIO buffer and write it to the response
    pdf = buffer.getvalue()
    buffer.close()
    
    # Create HTTP response with PDF
    response = HttpResponse(content_type='application/pdf')
    
    # Generate a filename
    filename = f"celio_emergency_card_{card.user.username}_{language}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    # Write PDF to response
    response.write(pdf)
    
    return response

def public_card(request, card_id):
    # Get the card by ID
    card = get_object_or_404(EmergencyCard, id=card_id)
    
    # Get requested language or default to card's language
    language = request.GET.get('lang', card.language)
    
    # Make sure language is available in translations
    if language not in card.translations and card.translations:
        language = next(iter(card.translations))
    
    return render(request, 'emergency_cards/public_card.html', {
        'card': card,
        'current_lang': language,
    })



@login_required
def share_card(request):
    # Get the user's card
    card = get_object_or_404(EmergencyCard, user=request.user)
    
    # Create a shareable URL for the public view
    share_url = request.build_absolute_uri(
        reverse('emergency_cards:public_card', args=[card.id])
    )
    
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(share_url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert the QR code to a data URL
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    qr_code_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
    qr_code_url = f"data:image/png;base64,{qr_code_data}"
    
    return render(request, 'emergency_cards/share.html', {
        'card': card,
        'share_url': share_url,
        'qr_code_url': qr_code_url,
    })

@login_required
def update_profile_picture(request):
    """Update the profile picture for the emergency card."""
    try:
        card = EmergencyCard.objects.get(user=request.user)
    except EmergencyCard.DoesNotExist:
        messages.error(request, "You need to create an emergency card first.")
        return redirect('emergency_cards:create_card')
    
    if request.method == 'POST' and request.FILES.get('profile_picture'):
        # Delete old profile picture if it exists to avoid storage bloat
        if card.profile_picture:
            card.profile_picture.delete(save=False)
        
        # Update with new profile picture
        card.profile_picture = request.FILES['profile_picture']
        card.save()
        
        messages.success(request, "Profile picture updated successfully.")
    
    return redirect('emergency_cards:themes')


@login_required
def apply_theme(request, theme_name):
    """Apply a selected theme to the emergency card."""
    try:
        card = EmergencyCard.objects.get(user=request.user)
    except EmergencyCard.DoesNotExist:
        messages.info(request, "You need to create an emergency card first.")
        return redirect('emergency_cards:create_card')
    
    # Get valid themes from the model choices
    valid_themes = [choice[0] for choice in EmergencyCard.THEME_CHOICES]
    
    # Validate the theme name
    if theme_name not in valid_themes:
        messages.error(request, f"Invalid theme selection: {theme_name}")
        return redirect('emergency_cards:card_detail')
    
    # Get language parameter
    language = request.GET.get('lang', 'EN')
    preview_only = request.GET.get('preview', 'false').lower() == 'true'
    
    # Only update the theme if not in preview mode
    if not preview_only:
        # Update the theme
        card.theme = theme_name
        card.save()
        messages.success(request, f"Theme updated to {theme_name.title()}")
    
    # Get the current language and message
    # Case insensitive comparison for language codes
    upper_lang = language.upper()
    
    # Get all available language keys in uppercase for comparison
    available_langs = {lang.upper(): lang for lang in card.translations.keys()}
    
    # Make sure requested language exists in translations
    if upper_lang in available_langs:
        language = available_langs[upper_lang]  # Use original case from card
    elif card.translations:
        language = next(iter(card.translations.keys()))
    
    # Get message in requested language
    message = card.get_message(language)
    
    # Get language display name
    current_lang_display = dict(EmergencyCard.LANGUAGE_CHOICES).get(language.lower(), language)
    
    # Create languages dictionary for the template
    languages = {}
    for lang_code in card.translations.keys():
        lang_name = dict(EmergencyCard.LANGUAGE_CHOICES).get(lang_code.lower(), lang_code)
        languages[lang_code] = lang_name
    
    if request.headers.get('HX-Request') or preview_only:  # if it's an HTMX request or preview
        # For preview mode, temporarily set the theme without saving it to the database
        original_theme = card.theme
        if preview_only:
            card.theme = theme_name  # Temporarily set the theme for rendering
        
        context = {
            'card': card,
            'current_lang': language,
            'current_lang_display': current_lang_display,
            'message': message,
            'languages': languages,
        }
        
        # Reset the theme to original if we're just previewing
        if preview_only:
            card.theme = original_theme
            
        # Return only the card preview
        return render(request, 'emergency_cards/partials/card_preview.html', context)
    
    return redirect('emergency_cards:card_detail')

@login_required
def themes(request):
    """Display available themes for the emergency card."""
    try:
        card = EmergencyCard.objects.get(user=request.user)
    except EmergencyCard.DoesNotExist:
        messages.info(request, "You need to create an emergency card first.")
        return redirect('emergency_cards:create_card')
    
    return render(request, 'emergency_cards/themes.html', {'card': card})

@login_required
def mark_tour_seen(request):
    """Mark the tour as seen by the user"""
    if request.method == 'POST':
        request.session['show_tour'] = False
        request.session.modified = True
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})