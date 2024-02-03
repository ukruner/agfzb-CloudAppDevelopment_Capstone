from django.contrib import admin
from .models import CarModel, CarMake, CarReview
import requests


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

class CarReviewAdmin(admin.ModelAdmin):
    actions = ['register_model_from_cloudant']
    def register_model_from_cloudant(modeladmin, request, queryset):
        # Check if 'id' is provided in request.GET
        if 'dealership' not in request.GET:
            modeladmin.message_user(request, "Please provide an 'id' parameter.", level='error')
            return

        # Getting the 'id' from request.GET
        provided_id = request.GET['dealership']

        # Making a call to the cloud database using 'id' as a query parameter
        api_url = 'https://*.cognitiveclass.ai/api/review'
        params = {'dealership': provided_id}
        response = requests.get(api_url, params=params)

        if response.status_code == 200:
            # Fetched data from cloudant
            cloud_data = response.json()
            for data in cloud_data:
                one_instance = CarReview(dealership=data['dealership'], name=data['name'], id=data['id'], review=data['review'], purchase=data['purchase'], purchase_date=data['purchase_date'], car_make=data['car_make'], car_model=data['car_model'], car_year=data['car_year'])
                one_instance.save()
            modeladmin.message_user(request, "Models registered successfully from cloudant.")
        else:
            modeladmin.message_user(request, "Error fetching data from cloudant.", level='error')

    register_model_from_cloudant.short_description = "Register review models from cloud cloudant database"

# Register models here
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarReview, CarReviewAdmin)