from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import CarDealer, CarReview, CarMake, CarModel
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import requests
from .restapis import get_dealers_from_cf, get_reviews_from_cf, post_request, analyze_review_sentiments
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
# Create an `about` view to render a static about page
# def about(request):
# ...


# Create a `contact` view to return a static contact page
#def contact(request):

# Create a `login_request` view to handle sign in request
# def login_request(request):

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
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/user_login.html', context)
    else:
        return render(request, 'djangoapp/user_login.html', context)

# Create a `logout_request` view to handle sign out request
# def logout_request(request):

def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
# def registration_request(request):
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
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
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        id = request.GET.get('id', '')  # Get id from request.GET, default to empty string if not provided
        state = request.GET.get('state', '')
        url = f"https://urmaskryner-3000.theiadockernext-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/dealership?id={id}&state={state}"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ', '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        context = {"dealerships": dealerships}
        return render(request, 'djangoapp/index.html', context)


def get_dealerships_by_id(id):
        url = f"https://urmaskryner-3000.theiadockernext-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/dealership?id={id}"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_name = dealerships[0]
        # Return a list of dealer short name
        return dealer_name

def review_template(request, id):
     
        dealerships = get_dealerships_by_id(id)

def add_review(request, id):
    url = 'https://urmaskryner-5000.theiadockernext-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/review'
    context = {}
    dealer_name = get_dealerships_by_id(id)
    context['dealer_name']=dealer_name
    context['dealer_id']=id
    if request.method == 'POST':
        if User.is_authenticated:
        #     # data = json.loads(request.body)
        #     review_date=datetime.utcnow().isoformat()
        #     review_content = request.POST("content")
        #     review_dealerid = id
        #     # car_id = request.POST["car"]
        #     # car = CarModel.objects.get(pk=car_id)
        #     # car_name = car.carmake.name
        #     # car_model_name = car.name
        #     # car_year = int(car.model_year.strftime("%Y"))
        #     review_purchase_tickbox = request.POST("purchasecheck")
        #     review_purchasedate = request.POST("purchasedate")
        #     review_body = dict()
        #     review_body = {"id":2323, "name":dealer_name,"review":review_content, "dealership":id, "purchase":review_purchase_tickbox, "purchase_date":review_purchasedate, "sentiment":analyze_review_sentiments(review_content)}
        #     data = json.dumps(review_body)
            # post_request(url, data)
            headers = {'Content-Type': 'application/json'}
            sample={
    "id": 34236,
    "name": "marianka",
    "dealership": 13,
    "review": "best ever, ever, ever service",
    "purchase": False,
    "purchase_date": "02/16/2021",
    "car_make": "Audi",
    "car_model": "Car",
    "car_year": 2021
}
            datasample = json.dumps(sample)
            response = requests.post(url, data=datasample, headers=headers)
            try:
                response.raise_for_status()
                print(response.text)
            except requests.exceptions.HTTPError as err:
                print(err)
            return redirect("djangoapp:dealer_details", id=id)
            # context['message']='Review posted succesfully'
            
            # if response.status_code == 200:
            #     # Handle successful response
            #     # For example, you could redirect or render a success message
            #     return HttpResponse("Review submitted successfully")
            # else:
            #     # Handle unsuccessful response
            #     # For example, you could render an error message
            #     return HttpResponse("Failed to submit review", status=response.status_code)
        else:
            context['message']="Only authenticated users can post reviews, please login"
            return render(request, 'djangoapp/login.html', context)
    elif request.method == "GET":
        
        cars = CarModel.objects.all()
        context['cars']=cars
        return render(request, 'djangoapp/add_review.html', context)
        # return HttpResponse("executing get request")

def get_reviews(request, id):
    if request.method == "GET":
        # id = request.GET.get('id')  
        url = f"https://urmaskryner-5000.theiadockernext-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/review?id={id}"
        # Get dealers from the URL
        reviews = get_reviews_from_cf(url)
        dealer_name = get_dealerships_by_id(id)
        # Concat all dealer's short name
        review_content = ', '.join([review.review for review in reviews])
        # Return a list of dealer short name
        context = {"reviews": reviews, "dealer_name": dealer_name}
        return render(request, 'djangoapp/dealer_details.html', context)

def about_us(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)

def contact_us(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

