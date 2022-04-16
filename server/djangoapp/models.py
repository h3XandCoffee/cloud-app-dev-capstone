from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
class CarMake (models.Model):
    make_name = models.CharField(null=False, max_length=160)
    make_description = models.TextField()

    def __str__(self):
        return "Make: " + self.make_name + ", " + \
               "Description: " + self.make_description


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    dealer_id = models.CharField(null=False, max_length=160)
    model_name = models.CharField(null=False, max_length=200)
    SEDAN = 'Sedan'
    SUV = 'SUV'
    WAGON = 'Wagon'
    COUPE = 'Coupe'
    CABRIO = 'Cabrio'
    MODEL_TYPE_CHOICES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'Wagon'),
        (COUPE, 'Coupe'),
        (CABRIO, 'Cabrio')
    ]
    model_type = models.CharField(
        null=False,
        max_length=20,
        choices=MODEL_TYPE_CHOICES,
        default=SEDAN
    )
    model_year = models.DateField(null=True)

    def __str__(self):
        return  "Model: " + self.model_name + ", " + \
                "Type: " + self.model_type + ", " + \
                "Year: " + self.model_year


# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:

    def __init__(self, id, city, state, st, address, zip, lat, long, short_name, full_name):
        # Dealer id
        self.id = id
        # Dealer city
        self.city = city
        # Dealer state
        self.state = state
        # Dealer state (short)
        self.st = st
        # Dealer address
        self.address = address
        # Dealer zip
        self.zip = zip
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer Full Name
        self.full_name = full_name

    def __str__(self):
        return "Dealer name: " + self.full_name


# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:

    def __init__(self, id, name, dealership, review, purchase, purchase_date, car_make, car_model, car_year, sentiment):
        # Review id
        self.id = id
        # Reviewer name
        self.name = name
        # Dealership id
        self.dealership = dealership
        # Review content
        self.review = review
        # Purchase
        self.purchase = purchase
        # Purchase date
        self.purchase_date = purchase_date
        # Car make
        self.car_make = car_make
        # Car model
        self.car_model = car_model
        # Car manufacturing year
        self.car_year = car_year
        # Review sentiment
        self.sentiment = sentiment

    def __str__(self):
        return  "Reviewer: " + self.name + ", " + \
                "Car make, model, and manufacturing year: " + self.car_make + self.car_model + self.car_year + ", " + \
                "Purchase date: " + self.purchase_date + ", " + \
                "Sentiment: " + self.sentiment + ", " + \
                "Review: " + self.review
