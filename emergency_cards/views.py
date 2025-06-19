import io
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render
from django.conf import settings
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
import json
import requests
from django.utils.translation import get_language_from_request

def translate_text(text, target_language, source_language='en'):
    """
    Mock translation function that provides realistic-looking translations for demo purposes.
    """
    if not text:
        return ''
    
    # Convert language codes to expected format (e.g., 'EN' -> 'en')
    target_language = target_language.lower()
    source_language = source_language.lower()
    
    # Don't translate if source and target are the same
    if source_language == target_language:
        return text
    
    # For demo purposes, provide complete translations for common medical phrases
    complete_translations = {
        'es': {
            'I have celiac disease': 'Tengo enfermedad celíaca',
            'I have celiac disease and cannot consume any amount of gluten': 'Tengo enfermedad celíaca y no puedo consumir ninguna cantidad de gluten',
            'In case of emergency, please ensure all food and medication is gluten-free': 'En caso de emergencia, por favor asegúrese de que todos los alimentos y medicamentos sean sin gluten',
            'I am allergic to gluten': 'Soy alérgico al gluten',
            'Please call my emergency contact': 'Por favor llame a mi contacto de emergencia',
        },
        'fr': {
            'I have celiac disease': 'Je souffre de maladie cœliaque',
            'I have celiac disease and cannot consume any amount of gluten': 'Je souffre de maladie cœliaque et ne peux consommer aucune quantité de gluten',
            'In case of emergency, please ensure all food and medication is gluten-free': 'En cas d\'urgence, veuillez vous assurer que tous les aliments et médicaments sont sans gluten',
            'I am allergic to gluten': 'Je suis allergique au gluten',
            'Please call my emergency contact': 'Veuillez appeler mon contact d\'urgence',
        },
        'de': {
            'I have celiac disease': 'Ich habe Zöliakie',
            'I have celiac disease and cannot consume any amount of gluten': 'Ich habe Zöliakie und kann keine Menge Gluten konsumieren',
            'In case of emergency, please ensure all food and medication is gluten-free': 'Im Notfall stellen Sie bitte sicher, dass alle Lebensmittel und Medikamente glutenfrei sind',
            'I am allergic to gluten': 'Ich bin allergisch gegen Gluten',
            'Please call my emergency contact': 'Bitte rufen Sie meinen Notfallkontakt an',
        },
        'zh': {
            'I have celiac disease': '我患有乳糜泻',
            'I have celiac disease and cannot consume any amount of gluten': '我患有乳糜泻，不能摄入任何含麸质的食物',
            'In case of emergency, please ensure all food and medication is gluten-free': '如遇紧急情况，请确保所有食物和药物都不含麸质',
            'I am allergic to gluten': '我对麸质过敏',
            'Please call my emergency contact': '请联系我的紧急联系人',
        }
    }
    
    # Fallback phrase dictionary
    phrase_dictionary = {
        'es': {
            'cannot consume': 'no puedo consumir',
            'any amount of gluten': 'ninguna cantidad de gluten',
            'in case of emergency': 'en caso de emergencia',
            'please ensure': 'por favor asegúrese',
            'food and medication': 'alimentos y medicamentos',
            'is gluten-free': 'sin gluten',
            'allergic': 'alérgico',
            'medical condition': 'condición médica',
            'emergency': 'emergencia'
        },
        'fr': {
            'cannot consume': 'ne peux pas consommer',
            'any amount of gluten': 'aucune quantité de gluten',
            'in case of emergency': 'en cas d\'urgence',
            'please ensure': 'veuillez vous assurer',
            'food and medication': 'nourriture et médicaments',
            'is gluten-free': 'sans gluten',
            'allergic': 'allergique',
            'medical condition': 'condition médicale',
            'emergency': 'urgence'
        },
        'de': {
            'cannot consume': 'kann nicht konsumieren',
            'any amount of gluten': 'keine Menge Gluten',
            'in case of emergency': 'im Notfall',
            'please ensure': 'bitte stellen Sie sicher',
            'food and medication': 'Essen und Medikamente',
            'is gluten-free': 'glutenfrei ist',
            'allergic': 'allergisch',
            'medical condition': 'medizinischer Zustand',
            'emergency': 'Notfall'
        },
        'zh': {
            'cannot consume': '不能食用',
            'any amount of gluten': '任何含麸质的食物',
            'in case of emergency': '如遇紧急情况',
            'please ensure': '请确保',
            'food and medication': '食物和药物',
            'is gluten-free': '不含麸质',
            'allergic': '过敏',
            'medical condition': '医疗状况',
            'emergency': '紧急情况'
        }
    }
    
    try:
        # First check if we have a complete translation for the whole text
        if target_language in complete_translations and text.lower() in complete_translations[target_language]:
            translated_text = complete_translations[target_language][text.lower()]
            print(f"DEBUG: Found complete translation for '{text[:30]}...' to {target_language}")
            return translated_text
            
        # If we have translations for this language but no exact match
        if target_language in phrase_dictionary:
            # First try to find the closest complete translation
            closest_match = None
            max_similarity = 0
            
            for eng_phrase in complete_translations.get(target_language, {}):
                # Simple overlap check - in a real system you'd use more sophisticated NLP
                if eng_phrase.lower() in text.lower() or text.lower() in eng_phrase.lower():
                    similarity = len(set(eng_phrase.lower().split()) & set(text.lower().split()))
                    if similarity > max_similarity:
                        max_similarity = similarity
                        closest_match = eng_phrase
            
            # If we found a reasonably close match, use its translation
            if closest_match and max_similarity > 2:
                translated_text = complete_translations[target_language][closest_match]
                print(f"DEBUG: Using close match translation for {target_language}")
                return translated_text
            
            # Otherwise do phrase-by-phrase translation
            words = text.split()
            result = []
            
            i = 0
            while i < len(words):
                # Try different phrase lengths
                translated = False
                for phrase_len in [3, 2, 1]:
                    if i + phrase_len <= len(words):
                        phrase = ' '.join(words[i:i+phrase_len]).lower()
                        if phrase in phrase_dictionary[target_language]:
                            result.append(phrase_dictionary[target_language][phrase])
                            i += phrase_len
                            translated = True
                            break
                
                # If no phrase match was found, keep the original word
                if not translated:
                    result.append(words[i])
                    i += 1
            
            translated_text = ' '.join(result)
            print(f"DEBUG: Translated phrase-by-phrase from {source_language} to {target_language}")
            return translated_text
        else:
            # For languages we don't have translations for
            print(f"DEBUG: No translations available for {target_language}, returning original text")
            return text
    except Exception as e:
        print(f"Translation error: {str(e)}")
        return text  # Return original text if translation fails


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
    This view now mirrors the clean_preview structure and styling.
    """
    card = get_object_or_404(EmergencyCard, user=request.user)
    
    # Determine the language to display
    requested_lang = request.GET.get('lang', card.preferred_language or 'en').lower()
    # Validate requested_lang against available choices
    valid_langs = [choice[0].lower() for choice in EmergencyCard.LANGUAGE_CHOICES]
    if requested_lang.lower() not in valid_langs:
        requested_lang = card.preferred_language.lower() if card.preferred_language else 'en' # Fallback
        
    current_lang = requested_lang # Keep it lowercase throughout
    
    # Get the theme from URL parameter or use card's theme as fallback
    requested_theme = request.GET.get('theme', card.theme or 'medical')
    valid_themes = ['dark', 'medical', 'minimal']
    if requested_theme not in valid_themes:
        requested_theme = card.theme or 'medical'  # Fallback to medical if no valid theme
    
    # Prepare language choices for the dropdown/switcher if needed
    language_choices = {code: name for code, name in EmergencyCard.LANGUAGE_CHOICES}
    current_lang_display = language_choices.get(current_lang, current_lang) # Get display name

    return render(request, 'emergency_cards/fullscreen_card.html', {
        'card': card,
        'theme': requested_theme,
        'current_lang': current_lang,
        'current_lang_display': current_lang_display,
        'language_choices': language_choices # Pass all choices for switcher
    })

@login_required
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
    """Apply a selected theme to the emergency card or preview it."""
    try:
        card = EmergencyCard.objects.get(user=request.user)
    except EmergencyCard.DoesNotExist:
        # Handle case where card doesn't exist - maybe redirect or show error
        # For preview, we might want a default/dummy card?
        # For now, let's assume the card exists for preview generation.
        # If called without a card, it should ideally not happen from the UI.
        # If it's not a preview, redirect as before.
        if not request.GET.get('preview'):
            messages.info(request, "You need to create an emergency card first.")
            return redirect('emergency_cards:create_card')
        else:
            # Handle preview request without a card - maybe return an error response
            # or a default placeholder? For now, returning error.
            return HttpResponse("Error: Card not found for preview.", status=404)

    valid_themes = [choice[0] for choice in EmergencyCard.THEME_CHOICES]
    if theme_name not in valid_themes:
        messages.error(request, f"Invalid theme selection: {theme_name}")
        # Redirect back to wherever the user was (e.g., detail or unified view)
        # Consider using request.META.get('HTTP_REFERER') or a specific view
        return redirect('emergency_cards:unified_card_management') # Redirect to unified view

    requested_lang_code = request.GET.get('lang') # Get requested language code (e.g., 'fr')
    preview_only = request.GET.get('preview', 'false').lower() == 'true'

    if not preview_only:
        card.theme = theme_name
        card.save()
        messages.success(request, f"Theme updated to {theme_name.title()}")
        return redirect('emergency_cards:unified_card_management') # Redirect after saving

    # --- Preview Logic --- 
    original_language = translation.get_language() # Remember original language
    requested_lang_upper = requested_lang_code.upper() if requested_lang_code else card.preferred_language.upper() if card.preferred_language else 'EN'
    
    # Determine the language to use for the preview context and translation activation
    # Priority: Requested 'lang' param -> Card preferred -> 'en'
    preview_lang_code = None
    available_langs_lower = {code.lower(): code for code, name in settings.LANGUAGES}
    
    if requested_lang_code and requested_lang_code.lower() in available_langs_lower:
        preview_lang_code = requested_lang_code.lower()
    elif card.preferred_language and card.preferred_language.lower() in available_langs_lower:
        preview_lang_code = card.preferred_language.lower()
    else:
        preview_lang_code = 'en' # Default to English

    print(f"Requested Language Code: {requested_lang_code}, Preview Language Code: {preview_lang_code}")

    # Get display name for the context
    current_lang_display = dict(settings.LANGUAGES).get(preview_lang_code, preview_lang_code.upper())
    
    context = {
        'card': card,
        'preview_theme': theme_name, # Pass the theme to apply in the template
        'current_lang': preview_lang_code.upper(), # Pass the language code (uppercase) for logic/display in template
        'current_lang_display': current_lang_display,
        # Add any other context needed by clean_preview.html
    }

    try:
        # Activate the requested language for this request thread
        translation.activate(preview_lang_code)
        
        # Render the preview template with the activated language
        html = render_to_string('emergency_cards/partials/clean_preview.html', context, request=request)
        
        return HttpResponse(html)
    finally:
        # Deactivate the language to revert to the original or default
        translation.deactivate()

    # Fallback redirect if something goes wrong, though HttpResponse should be returned above
    return redirect('emergency_cards:unified_card_management')


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
    
    def prepare_preview_context(request, card, current_lang):
        """
        Prepares the context dictionary for rendering a card preview.
        
        Args:
            request: The HttpRequest object
            card: The EmergencyCard instance or None
            current_lang: The current language code (e.g., 'en', 'es')
        
        Returns:
            dict: Context dictionary for the preview template
        """
        # Ensure current_lang is lowercase for consistency
        current_lang = current_lang.lower()
        
        # Default theme if card doesn't exist
        preview_theme = request.POST.get('preview_theme', card.theme if card else 'minimal')
        
        # If no card, return default empty context
        if not card:
            return {
                'card': None,
                'current_lang': current_lang,
                'current_lang_display': dict(EmergencyCard.LANGUAGE_CHOICES).get(current_lang, current_lang),
                'user': request.user,
                'preview_theme': preview_theme,
                'language_choices': EmergencyCard.LANGUAGE_CHOICES,
                'translations': {},
                'message': 'No card information yet.',
                'medical_bullets': [],
                'is_translated': False,
                'user_name': request.user.get_full_name() or request.user.username
            }
        
        # Get the message for the current language (predefined + custom note)
        message = card.get_message(current_lang)  
        
        # Get medical info bullets for this condition and language
        medical_bullets = card.get_medical_info_bullets(current_lang)
        print(f"DEBUG: Medical bullets for {current_lang}: {medical_bullets}")
        
        # Check if we're viewing a translation (current language differs from preferred)
        is_translated = current_lang != card.preferred_language.lower()
        
        return {
            'card': card,
            'current_lang': current_lang,
            'current_lang_display': dict(EmergencyCard.LANGUAGE_CHOICES).get(current_lang, current_lang),
            'user': request.user,
            'preview_theme': preview_theme,
            'language_choices': EmergencyCard.LANGUAGE_CHOICES,
            'translations': card.translations if card.translations else {},
            'message': message,
            'medical_bullets': medical_bullets,
            'is_translated': is_translated,
            'user_name': card.user_name or request.user.get_full_name() or request.user.username,
            'custom_note': card.get_custom_note(current_lang)
        }

    # Check if this is a request to get message for a specific language
    if request.method == 'GET' and request.GET.get('get_message') == 'true' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        lang = request.GET.get('lang', 'en').lower()
        
        if not card:
            return JsonResponse({
                'success': False,
                'message': 'No card found'
            })
        
        # Get the full message (predefined + custom note) for the language
        message = card.get_message(lang)
        
        # Also get custom note separately
        custom_note = card.get_custom_note(lang)
        
        return JsonResponse({
            'success': True,
            'message': message,
            'customNote': custom_note,
            'isTranslated': lang != card.preferred_language.lower(),
            'medicalBullets': card.get_medical_info_bullets(lang)
        })
    
    # Get or create a form instance
    if request.method == 'POST':
        # Check if this is a language switch request
        if request.POST.get('switch_language') == 'true':
            # First check if there's a lang in the GET parameters as it takes precedence
            if 'lang' in request.GET:
                current_lang = request.GET.get('lang', 'en').lower()
            else:
                current_lang = request.POST.get('active_language', 'en').lower()
            
            previous_lang = request.POST.get('previous_language', 'en').lower()
            print(f"DEBUG: Switch language - from {previous_lang} to {current_lang}")
            
            # Check if we have an updated custom note from the form
            custom_note_field_name = f'custom_note_{previous_lang}'
            if custom_note_field_name in request.POST:
                # Get the custom note from the form
                custom_note_from_form = request.POST.get(custom_note_field_name, '').strip()
                
                # Update the custom note for the previous language
                if card and custom_note_from_form:
                    card.set_custom_note(previous_lang, custom_note_from_form)
                    card.save()
            
            # Handle translation of custom note to the current language
            if card:
                # Get the custom note for the previous language
                custom_note = card.get_custom_note(previous_lang)
                
                # If there's a custom note in the previous language and no translation yet for current language
                # or we're forcing a retranslation
                needs_translation = custom_note and (current_lang not in card.translations or 
                                                  request.POST.get('force_retranslate') == 'true')
                
                if needs_translation:
                    # Translate the custom note to the current language
                    translated_note = translate_text(
                        custom_note,
                        target_language=current_lang,
                        source_language=previous_lang
                    )
                    
                    # Store the translation
                    if translated_note:
                        card.set_custom_note(current_lang, translated_note)
                        card.save()
            
            # Update card's preferred language
            if card:
                card.preferred_language = current_lang
                
                # Force save language selection and reset any language cookies if requested
                if request.POST.get('force_language_update') == 'true':
                    # Explicitly set language to ensure it takes precedence
                    card.language = current_lang
                    
                card.save(update_fields=['preferred_language', 'language'])
                print(f"DEBUG: Updated card preferred language during AJAX to: {card.preferred_language}")
            
            # Prepare context for preview
            preview_context = prepare_preview_context(request, card, current_lang)
            
            # Activate the requested language for template rendering
            from django.utils import translation
            # Convert the language code to lowercase for Django's translation system
            lang_code = current_lang.lower()
            print(f"DEBUG: Activating language: {lang_code} for template rendering")
            
            # Save current language
            old_language = translation.get_language()
            
            try:
                # Activate the new language
                translation.activate(lang_code)
                
                # Render the template with the activated language
                response = render(request, 'emergency_cards/partials/clean_preview.html', preview_context)
                
                # Set the language cookie
                response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)
                
                return response
            finally:
                # Restore original language
                translation.activate(old_language)
        
        # Regular form submission or theme change
        form = EmergencyCardForm(request.POST, request.FILES, instance=card)
        if form.is_valid():
            try:
                card = form.save(commit=False)
                card.user = request.user
                
                # Get current language from form
                current_lang = request.POST.get('active_language', 'en').lower()
                
                # Handle custom note if provided
                custom_note = request.POST.get('custom_note', '').strip()
                if custom_note:
                    # Set the custom note for the current language
                    card.set_custom_note(current_lang, custom_note)
                    
                # Set as preferred language if it's changed
                if card.preferred_language != current_lang:
                    card.preferred_language = current_lang
                
                # Save the card
                card.save()
                
                # Process the profile picture if needed
                if 'profile_picture' in request.FILES:
                    card.profile_picture = request.FILES['profile_picture']
                    card.save()
                
                # Check if show_profile_pic preference changed
                show_pic = request.POST.get('show_profile_pic')
                card.show_profile_pic = show_pic == 'on'
                card.save()
                
                messages.success(request, 'Your emergency card has been saved successfully!')
                return redirect('emergency_cards:unified_card_management')
                
            except Exception as e:
                # Log the error for debugging
                print(f"Error saving emergency card: {str(e)}")
                messages.error(request, f'An error occurred while saving your card: {str(e)}')
        else:
            # If form is not valid, show error messages
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = EmergencyCardForm(instance=card)
        
    # Set initial values for new card
    if not card and not request.method == 'POST':
        form.initial = {
            'theme': 'light',
            'preferred_language': 'en',
            'show_profile_pic': True,
            'condition': 'CEL'  # Default to Celiac Disease
        }
        
    # Get current language - either from the card's preference or default to English    
    current_lang = card.preferred_language.lower() if card else 'en'
    
    # If GET request has a lang parameter, update current_lang
    if 'lang' in request.GET:
        # Get the language from request, default to 'en' (lowercase), and convert to lowercase
        current_lang = request.GET.get('lang', 'en').lower()
        print(f"DEBUG: Language from GET parameter: {current_lang}")
        if card:
            # Force update the preferred language and save
            card.preferred_language = current_lang
            # Also update the language field to ensure consistency
            card.language = current_lang
            card.save(update_fields=['preferred_language', 'language'])
            print(f"DEBUG: Updated card preferred language to: {card.preferred_language}")
            
            # Reset any cookies that might be affecting language selection
            from django.utils import translation
            translation.activate(current_lang)
    
    # Get language display name for the current language
    current_lang_display = dict(EmergencyCard.LANGUAGE_CHOICES).get(current_lang.lower(), current_lang)
    
    print(f"DEBUG: Current Language: {current_lang}, Display: {current_lang_display}")
    
    # Prepare context for template rendering
    context = {
        'form': form,
        'card': card,
        'page_title': 'My Emergency Card',
        'current_lang': current_lang,
        'current_lang_display': current_lang_display,
        'language_choices': EmergencyCard.LANGUAGE_CHOICES,
        'user': request.user,
        'show_tour': request.session.get('show_tour', True),
        'translations': card.translations if card else {},
    }
    
    # Activate Django translation for this request
    from django.utils import translation
    old_language = translation.get_language()
    try:
        # Activate the user's selected language
        translation.activate(current_lang)
        # Render the template with the activated language
        response = render(request, 'emergency_cards/unified_card_management.html', context)
        # Set the language cookie
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, current_lang)
        return response
    finally:
        # Restore original language
        translation.activate(old_language)

@login_required
def translate_card(request):
    """
    API endpoint to translate a card without requiring a full page reload.
    Returns only the necessary data as JSON.
    """
    # Get the languages from the request
    from_lang = request.GET.get('from_lang', 'en').lower()
    to_lang = request.GET.get('to_lang', 'en').lower()
    
    # Debugging
    print(f"DEBUG: Translating card from {from_lang} to {to_lang}")
    
    # Get the user's card
    card = EmergencyCard.objects.filter(user=request.user).first()
    
    if not card:
        return JsonResponse({
            'success': False,
            'error': 'No card found'
        })
    
    # Save the current custom note if it exists in the request
    custom_note_param = f'custom_note_{from_lang}'
    if request.method == 'POST' and custom_note_param in request.POST:
        card.set_custom_note(from_lang, request.POST.get(custom_note_param))
        card.save()
    
    # Get the translated message and medical bullets
    translated_message = card.get_message(to_lang)
    medical_bullets = card.get_medical_info_bullets(to_lang)
    custom_note = card.get_custom_note(to_lang)
    
    # Update the card's preferred language
    card.preferred_language = to_lang
    card.save()
    
    # Prepare the context for rendering the card
    context = prepare_preview_context(request, card, to_lang)
    
    # Render just the card HTML
    from django.template.loader import render_to_string
    from django.utils import translation
    
    # Activate the target language for template rendering
    old_language = translation.get_language()
    try:
        translation.activate(to_lang)
        card_html = render_to_string(
            'emergency_cards/partials/clean_preview.html',
            context
        )
    finally:
        translation.activate(old_language)
    
    # Return the translated data as JSON
    return JsonResponse({
        'success': True,
        'card_html': card_html,
        'message': translated_message,
        'custom_note': custom_note,
        'medical_bullets': medical_bullets,
        'current_lang': to_lang,
        'current_lang_display': dict(EmergencyCard.LANGUAGE_CHOICES).get(to_lang, to_lang)
    })