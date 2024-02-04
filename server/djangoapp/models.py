from django.db import models
from django.utils.timezone import now

# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object

class CarMake(models.Model):
    name = models.CharField(null=False, max_length=50, default='enter car make')
    country_origin = models.CharField(null=False, max_length=50, default='country of origin')
    desc = models.CharField(max_length=1000)
    def __str__(self):
        return "Car make: " + self.name + "," + \
                "Country of origin: " + self.country_origin + "," + \
               "Description: " + self.desc    


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object

class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete = models.CASCADE)
    dealer_id = models.IntegerField()
    model_name = models.CharField(null=False, max_length=50, default='enter car model')
    SEDAN = "sedan"
    SUV = "suv"
    WAGON = "wagon"
    HATCHBACK = "hatchback"
    UNIVERSAL = "universal"
    MINIVAN = "minivan"
    CABRIOLET = "cabriolet"
    MODEL_CHOICES = [
        (SEDAN, "Sedan"),
        (SUV, "SUV"),
        (WAGON, "WAGON"),
        (HATCHBACK, "Hatchback"),
        (UNIVERSAL, "Universal"),
        (MINIVAN, "Minivan"),
        (CABRIOLET, "Cabriolet")
    ]
    model_type = models.CharField(
        null=False,
        max_length=20,
        choices=MODEL_CHOICES,
        default=SEDAN
    )
    model_year = models.DateField()
    is_used = models.BooleanField(default=False)
    def __str__(self):
        return "Car make: " + self.car_make.name + "," + \
        "Car model: " + self.model_name + "," + \
        "Car dealership id: " + str(self.dealer_id) + "," + \
        "Car type: " + self.model_type + "," + \
        "Car year: " + str(self.model_year) + "," + \
        "Car new or not: " + str(self.is_used) + "," + \
        f"Car images are available on URL https://www.google.com/search?q={self.car_make.name}+{self.model_name}&tbm=isch"

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
class CarReview(models.Model):
    dealership = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, default='', blank=True)
    id = models.IntegerField(blank=True, null=True)
    review = models.TextField(max_length=500, blank=True, null=True)
    purchase = models.BooleanField(blank=True, null=True)
    purchase_date = models.CharField(max_length=30, blank=True, null=True)
    car_make = models.CharField(max_length=50, blank=True, null=True)
    car_model = models.CharField(max_length=50, blank=True, null=True)
    car_year = models.IntegerField(blank=True, null=True)

    # def save(self, *args, **kwargs):
    #     api_url = 'https://*.cognitiveclass.ai/api/review' 
    #     response = requests.get(api_url)
    #     if response.status_code == 200:
    #         models_data = response.json()
    #         for model_data in models_data:
    #             dealership = model_data.get('dealership')
    #             name = model_data.get('name')
    #             id = model_data.get('id')
    #             review = model_data.get('review')
    #             purchase = model_data.get('purchase')
    #             purchase_date = model_data.get('purchase_date')
    #             car_make = model_data.get('car_make')
    #             car_model = model_data.get('car_model')
    #             car_year = model_data.get('car_year')
                
    #             # Creating the CarReview instance
    #             one_instance = CarReview(dealership=dealership, name=name, id=id, review=review, purchase=purchase, purchase_date=purchase_date, car_make=car_make, car_model=car_model, car_year=car_year)
    #             one_instance.save()
    #     else:
    #         print('Error fetching models from cloud database')
    #     super().save(*args, **kwargs)

    def __str__(self):
        return f"Reviews of the car dealership with id of {str(self.dealership)}: "