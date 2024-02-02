from django.contrib import admin
from .models import CarModel, CarMake


# Register your models here.

class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 1
# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    fields = ["car_make", "dealer_id", "model_name", "model_type", "model_year", "is_used"]

# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    fields = ["name", "country_origin", "desc"]
    inlines = [CarModelInline]

# Register models here
admin.site.register(CarMake, CarMakeAdmin)