from django import template
register = template.Library()

@register.filter(name='addclass')
def addclass(field, css):
    if hasattr(field, 'as_widget'):
        return field.as_widget(attrs={"class": css})
    else:
        # If field is not a form field (e.g., it's a string), just return it
        return field