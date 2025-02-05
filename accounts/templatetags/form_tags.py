from django import template

register = template.library()

@register.filter(name='addclass')
def addclass(field, css):
    return field.as_widget(attrs={"class": css})