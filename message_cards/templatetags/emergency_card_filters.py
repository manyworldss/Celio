from django import template

register = template.Library()

@register.filter
def get_message(card, language_code='en'):
    """
    Template filter to get the message for a card in the specified language.
    Usage: {{ card|get_message:language_code }}
    """
    if card is None:
        return ""
    
    return card.get_message(language_code)

@register.filter
def get_custom_note(card, language_code='en'):
    """
    Template filter to get the custom note for a card in the specified language.
    Usage: {{ card|get_custom_note:language_code }}
    """
    if card is None:
        return ""
    
    return card.get_custom_note(language_code)

@register.filter
def get_medical_info_bullets(card, language_code='en'):
    """
    Template filter to get the medical info bullets for a card in the specified language.
    Usage: {{ card|get_medical_info_bullets:language_code }}
    """
    if card is None:
        return []
    
    return card.get_medical_info_bullets(language_code)