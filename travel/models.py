from django.db import models
from django.utils.translation import gettext_lazy as _

# travel/models.py
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

class Country(models.Model):
    """Model for storing country information"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    code = models.CharField(max_length=2, unique=True)  # ISO country code (e.g., US, JP, FR)
    flag_emoji = models.CharField(max_length=10, blank=True)  # Flag emoji for display
    language = models.CharField(max_length=100)  # Primary language
    language_code = models.CharField(max_length=2)  # ISO language code (e.g., en, ja, fr)
    celiac_awareness = models.IntegerField(
        choices=[
            (1, _('Very Low')),
            (2, _('Low')),
            (3, _('Moderate')),
            (4, _('High')),
            (5, _('Very High')),
        ],
        default=3
    )
    color = models.CharField(max_length=7, default="#808080", help_text="Hex color code for the country card")
    
    # General information fields
    summary = models.TextField(help_text=_("General information about celiac awareness in this country"))
    dining_tips = models.TextField(help_text=_("Tips for dining safely in this country"))
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Countries"
        ordering = ['name']

class DishesToAvoid(models.Model):
    """Model for storing dishes to avoid in specific countries"""
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='dishes_to_avoid')
    name = models.CharField(max_length=100)
    local_name = models.CharField(max_length=100, blank=True, help_text=_("Name in local language"))
    description = models.TextField()
    ingredients = models.TextField(help_text=_("Common ingredients that contain gluten"))
    
    def __str__(self):
        return f"{self.name} ({self.country.name})"
    
    class Meta:
        verbose_name_plural = "Dishes to Avoid"

class RestaurantPhrase(models.Model):
    """Model for storing useful restaurant phrases"""
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='restaurant_phrases')
    english_text = models.TextField()
    translated_text = models.TextField(help_text=_("Translation in local language"))
    pronunciation = models.TextField(blank=True, help_text=_("Pronunciation guide if applicable"))
    category = models.CharField(
        max_length=20,
        choices=[
            ('general', _('General')),
            ('ordering', _('Ordering')),
            ('ingredients', _('Ingredients')),
            ('emergency', _('Emergency')),
        ],
        default='general'
    )
    
    def __str__(self):
        return f"{self.english_text[:30]}... ({self.country.name})"
# Create your models here.
