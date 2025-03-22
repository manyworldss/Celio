from django.contrib import admin
from .models import Country, DishesToAvoid, RestaurantPhrase

class DishesToAvoidInline(admin.TabularInline):
    model = DishesToAvoid
    extra = 1

class RestaurantPhraseInline(admin.TabularInline):
    model = RestaurantPhrase
    extra = 1

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'flag_emoji', 'language', 'celiac_awareness')
    search_fields = ('name', 'language')
    list_filter = ('celiac_awareness',)
    inlines = [DishesToAvoidInline, RestaurantPhraseInline]

@admin.register(DishesToAvoid)
class DishesToAvoidAdmin(admin.ModelAdmin):
    list_display = ('name', 'local_name', 'country')
    search_fields = ('name', 'local_name', 'description')
    list_filter = ('country',)

@admin.register(RestaurantPhrase)
class RestaurantPhraseAdmin(admin.ModelAdmin):
    list_display = ('english_text', 'country', 'category')
    search_fields = ('english_text', 'translated_text')
    list_filter = ('country', 'category')

