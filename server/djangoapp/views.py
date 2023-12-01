from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarModel
from .restapis import get_dealers_by_id_from_cf, get_dealers_from_cf, get_dealers_reviews_from_cf
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page

def get_about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)

# Create a `contact` view to return a static contact page
def get_contact_us(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact_us.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/index.html', context)


# ...

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')
# ...

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/regestration.html', context)
# ...

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships_by_id(request, dealer_id):
    print("dg")
    if request.method == "GET":
        url = "http://127.0.0.1:3000/dealerships/get"
    
    # Get dealers from the URL
    dealerships = get_dealers_by_id_from_cf(url,dealer_id=dealer_id)
    print(dealerships)
    # Concat all dealer's short name
    dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
    # Return a list of dealer short name
    return HttpResponse(dealer_names)

def get_dealerships(request):
    print("dg")
    if request.method == "GET":
        url = "http://127.0.0.1:3000/dealerships/get"
    
    # Get dealers from the URL
    dealerships = get_dealers_from_cf(url)
    print(dealerships)
    # Concat all dealer's short name
    dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
    # Return a list of dealer short name
    return HttpResponse(dealer_names)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

def get_dealer_details(request,dealer_id):
    if request.method == "GET":
        url = "http://127.0.0.1:5000/api/get_reviews"
    
    # Get dealers from the URL
    reviews = get_dealers_reviews_from_cf(url,dealer_id=dealer_id)
    # Concat all dealer's short name
    #dealer_name = ' '.join([dealer.short_name for dealer in dealerships])
    # Return a list of dealer short name
    return HttpResponse(reviews)

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

def add_review(request, dealer_id):
    if request.method == "GET":
        cars = CarModel.objects.filter(dealer_id=dealer_id)
        context = {
            "cars": cars,
            "dealer_id": dealer_id,
        }
        return render(request, "djangoapp/add_review.html", context)

    
    if request.method == "POST":
        url = "http://127.0.0.1:5000/api/post_review"
        review = {}
        input_data = request.POST
        review["dealership"] = int(dealer_id)
        review["review"] = input_data["content"]
        review["purchase"] = input_data.get("purchasecheck", False)
        review["purchase_date"] = input_data["purchasedate"]
        car = CarModel.objects.get(pk=input_data["car"])
        if car:
            review["car_make"] = car.CarMake.name
            review["car_model"] = car.name
            review["car_year"] = car.year.strftime("%Y")
        else:
            review["car_make"] = "None"
            review["car_model"] = "None"
            review["car_year"] = "None"
        
        review["name"] = "name"
        review["id"] = 1
        json_payload = {"review": review}
        print(json_payload)
        #post_review(url, json_payload)
        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)

