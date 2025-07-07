from django import template
import colorsys

register = template.Library()

@register.filter
def darken(hex_color, amount=0.2):
    """
    Darken a hex color by the specified amount (0.0 to 1.0)
    """
    if not hex_color or not hex_color.startswith('#'):
        return hex_color
    
    # Remove the # symbol
    hex_color = hex_color.lstrip('#')
    
    # Convert hex to RGB
    try:
        r = int(hex_color[0:2], 16) / 255.0
        g = int(hex_color[2:4], 16) / 255.0
        b = int(hex_color[4:6], 16) / 255.0
    except (ValueError, IndexError):
        return hex_color
    
    # Convert RGB to HSV
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    
    # Darken by reducing the value (brightness)
    v = max(0, v - amount)
    
    # Convert back to RGB
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    
    # Convert to hex
    r = int(r * 255)
    g = int(g * 255)
    b = int(b * 255)
    
    return f'#{r:02x}{g:02x}{b:02x}'