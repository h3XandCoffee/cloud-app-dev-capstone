from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarDealer, CarMake, CarModel
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, get_dealer_by_id, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
def static(request):
    context = {}
    return render(request, 'djangoapp/static.html', context)


# Create an `about` view to render a static about page
def about(request):
    context = {}
    return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    return render(request, 'djangoapp/contact.html', context)


# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            return render(request, 'djangoapp/index.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    print("Log out the user `{}`".format(request.user.username))
    logout(request)
    return redirect('djangoapp:index')


# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)

    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False

        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.debug("{} is new user".format(username))

        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            return render(request, 'djangoapp/registration.html', context)


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        url = "https://0e97e6bd.eu-gb.apigw.appdomain.cloud/api/dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ', '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        context = { 'dealership_list': dealerships }
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
#   if request.method == "GET":
    url = "https://0e97e6bd.eu-gb.apigw.appdomain.cloud/api/review"
    # Get dealers from the URL
    reviews = get_dealer_reviews_from_cf(url, dealer_id=dealer_id)
    # Concat all dealer's short name
    reviews_content = ', '.join([review.name + ' for ' + str(review.dealership) + ': ' + review.review + '(' + review.review + ')' for review in reviews])
    # Return a list of reviews for the given dealership
    context = { 'reviews': reviews, 'dealer_id': dealer_id }
    return render(request, 'djangoapp/dealer_details.html', context)


# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
def add_dealer_review(request, dealer_id): 
    context = {}
    context['dealer_id'] = dealer_id

    # get dealer
    url = "https://0e97e6bd.eu-gb.apigw.appdomain.cloud/api/dealership"
    dealer = get_dealer_by_id(url, dealer_id = dealer_id)
    context['dealer'] = dealer

    if request.method == "GET":
        # get cars
        cars = CarModel.objects.filter(dealer_id = dealer_id)
        context['cars'] = cars

    if request.method == "POST" and User.is_authenticated:
        # get cars
        car = CarModel.objects.filter(id = request.POST['car'])
        review = {
            # Reviewer name
            'name': request.user.first_name + request.user.last_name,
            # Dealership id
            'dealership': dealer_id,
            # Review content
            'review': request.POST['content'],
            # Purchase
            'purchase': request.POST['purchasecheck'],
            # Purchase date
            'purchasedate': request.POST['purchasedate'],
            # Car make
            'car_make': car[0].car_make.make_name,
            # Car model
            'car_model': car[0].model_name,
            # Car manufacturing year
            'car_year': car[0].model_year,
            # Review sentiment
            'sentiment': "neutral"
            # Review time
            #'time': datetime.utcnow().isoformat()
        }

        url = "https://0e97e6bd.eu-gb.apigw.appdomain.cloud/api/review"
        post_request(url, review)
        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)

    return render(request, 'djangoapp/add_review.html', context)
