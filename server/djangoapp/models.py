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


# <HINT> Create a plain Python class `DealerReview` to hold review data
