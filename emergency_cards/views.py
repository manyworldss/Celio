import io
from django.http import HttpResponse
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import EmergencyCard

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
    language = request.GET.get('lang','EN') # default to english if no language specified
    # get message in requested language
    message = card.get_message(language)
    if request.headers.get('HX-Request'): # if it's an HTMX request return just the message
     # return formatted message content
        return render(request, 'emergency_cards/card_detail.html', {'message': message, 'card': card, 'theme': card.theme})
    # for regular requests, redirect to card detail with language parameter
    return redirect(f"emergency_cards:card_detail?lang={language}")


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
    card = get_object_or_404(EmergencyCard, user=request.user)
    return render(request, 'emergency_cards/card_detail.html', {'card': card})

    # get the current language from request or default to card language
    current_lang = request.GET.get('lang', card.language)

    if current_lang not in card.translations and card.translations:
        current_lang = next(iter(card.translations))

    return render(request, 'emergency_cards/card_detail.html', {'card': card, 'current_language': current_lang})

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
    language = request.GET.get('lang', card.language)
    
    # For wallet cards, will implement this later
    if format_type == 'wallet':
        # Placeholder for wallet card functionality
        return render(request, 'emergency_cards/modals/download_modal.html', {
            'card': card,
            'error': 'Wallet card format is coming soon!'
        })
    
    # For showing the modal via HTMX
    if request.headers.get('HX-Request') and not request.GET.get('download', ''):
        return render(request, 'emergency_cards/modals/download_modal.html', {'card': card})
    
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
    card = get_object_or_404(EmergencyCard, user=request.user)
    
    # Create a public shareable URL
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
    
    # Return modal template with context
    if request.headers.get('HX-Request'):
        return render(request, 'emergency_cards/modals/share_modal.html', {
            'card': card,
            'share_url': share_url,
            'qr_code_url': qr_code_url,
        })
    
    # For non-HTMX requests, redirect to card detail
    return redirect('emergency_cards:card_detail')