from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    Template filter to access dictionary items by key
    Usage: {{ mydict|get_item:key_variable }}
    """
    if dictionary is None:
        return ""
    
    return dictionary.get(key, "")

@register.filter
def get_dict_value(dictionary, key):
    """
    Template filter to access dictionary items by key
    Alternative name for the same functionality as get_item
    Usage: {{ mydict|get_dict_value:key_variable }}
    """
    if dictionary is None:
        return ""
    
    return dictionary.get(key, "")
