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
    """
    Legacy view for creating/editing emergency cards.
    Now redirects to the unified card management page.
    """
    # Redirect to the unified card management view
    return redirect('emergency_cards:unified_card_management')


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
    """
    Legacy view for displaying emergency card details.
    Now redirects to the unified card management page.
    """
    # Redirect to the unified card management view
    return redirect('emergency_cards:unified_card_management')


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

@login_required
def fullscreen_card(request):
    """
    Display a fullscreen view of the user's emergency card.
    Simplified to remove language switching functionality.
    """
    try:
        card = EmergencyCard.objects.get(user=request.user)
    except EmergencyCard.DoesNotExist:
        # If user doesn't have a card yet, redirect to unified card management
        return redirect('emergency_cards:unified_card_management')
    
    # Always use the user's preferred language for the fullscreen view
    current_lang = card.preferred_language or 'EN'
    
    # Get the message for the current language
    message = card.translations.get(current_lang, card.translations.get('EN', ''))
    
    context = {
        'card': card,
        'current_lang': current_lang,
        'message': message,
    }
    
    return render(request, 'emergency_cards/fullscreen_card.html', context)

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

@login_required
def unified_card_management(request):
    """
    Unified view for creating, editing, and managing emergency cards.
    This view combines card creation, theme selection, and language switching 
    into a single interface with live preview functionality.
    """
    try:
        card = EmergencyCard.objects.get(user=request.user)
    except EmergencyCard.DoesNotExist:
        card = None
    
    # Get the active language (default to EN if not provided)
    active_language = request.POST.get('active_language', 'EN').upper()
    
    # Check if we're switching languages
    if request.POST.get('switch_language', False):
        active_language = request.POST.get('language-selector', 'EN').upper()
    
    # Check if we're just previewing a theme
    preview_theme = request.POST.get('preview_theme', False)
    
    if preview_theme and card:
        # For theme preview, we just want to update the card preview with the selected theme
        theme = request.POST.get('theme')
        
        # Get the appropriate message based on the active language
        message = ""
        if card.translations and active_language in card.translations:
            message = card.translations[active_language]
        elif card.translations and 'EN' in card.translations:
            message = card.translations['EN']
        
        return render(request, 'emergency_cards/partials/card_preview.html', {
            'card': card,
            'message': message,
            'current_lang': active_language,
            'preview_theme': theme,
        })
    
    if request.method == 'POST' and not preview_theme and not request.POST.get('switch_language', False):
        if card:  # if card exists, update it
            form = EmergencyCardForm(request.POST, request.FILES, instance=card)
        else:
            form = EmergencyCardForm(request.POST, request.FILES)
        
        if form.is_valid():
            card = form.save(commit=False)
            card.user = request.user
            
            # Initialize translations dictionary if needed
            if not card.translations:
                card.translations = {}
            
            # Process all language texts from the form
            for lang_code, _ in EmergencyCard.LANGUAGE_CHOICES:
                lang_code = lang_code.upper()
                message_field_name = f'message_{lang_code.lower()}'
                
                if message_field_name in request.POST and request.POST[message_field_name].strip():
                    # Save the message text for this language
                    card.translations[lang_code] = request.POST[message_field_name].strip()
            
            # Set the preferred language based on the active tab
            card.preferred_language = active_language
            
            # Save selected theme
            if 'theme' in request.POST:
                card.theme = request.POST.get('theme')
            
            # Make sure at least one language translation exists (English)
            if not card.translations or 'EN' not in card.translations:
                if 'message_en' in request.POST and request.POST['message_en'].strip():
                    card.translations['EN'] = request.POST['message_en'].strip()
                else:
                    card.translations['EN'] = "I have celiac disease/gluten sensitivity and cannot consume any foods containing gluten."
            
            card.save()
            
            messages.success(request, "Your emergency card has been saved successfully!")
            return redirect('emergency_cards:unified_card_management')
    else:
        # If user has a card, fill form with existing data
        if card:
            # Pre-populate form with card data
            form = EmergencyCardForm(instance=card)
        else:
            # Create blank form
            form = EmergencyCardForm()
    
    # Get current language for the active tab (default to English)
    current_lang = active_language
    if card and card.preferred_language and not request.POST.get('switch_language', False):
        current_lang = card.preferred_language
    
    # If GET request has a lang parameter, update current_lang
    if 'lang' in request.GET:
        current_lang = request.GET.get('lang', 'EN').upper()
    
    # For HTMX requests that are switching languages, render just the card preview
    if request.POST.get('switch_language', False):
        message = ""
        if card and card.translations and active_language in card.translations:
            message = card.translations[active_language]
        elif card and card.translations and 'EN' in card.translations:
            message = card.translations['EN']
        
        return render(request, 'emergency_cards/partials/card_preview.html', {
            'card': card,
            'message': message,
            'current_lang': active_language,
        })
    
    return render(request, 'emergency_cards/unified_card_management.html', {
        'form': form,
        'card': card,
        'page_title': 'My Emergency Card',
        'current_lang': current_lang,
        'language_choices': EmergencyCard.LANGUAGE_CHOICES,
    })