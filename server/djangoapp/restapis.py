import requests
import json
from .models import CarDealer, CarReview
from requests.auth import HTTPBasicAuth
from cloudant.client import Cloudant
from cloudant.query import Query
from ibm_cloud_sdk_core import ApiException
import atexit


#sorting out cloudant
cloudant_username = "7aa5ee38-cc9d-4038-8268-a931081002b2-bluemix"
cloudant_api_key = "FA83yCzfYzrd0XRoNkHYpyqoX_L_jEIFjYoQmbUX97Dk"
cloudant_url = "https://7aa5ee38-cc9d-4038-8268-a931081002b2-bluemix.cloudantnosqldb.appdomain.cloud"
client = Cloudant.iam(cloudant_username, cloudant_api_key, connect=True, url=cloudant_url)

session = client.session()

db_dealerships = client['dealerships']
db_reviews = client['reviews']

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


def get_dealers_from_cf():
    model_results = []
    for dealer_doc in db_dealerships:
        dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                    id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                    short_name=dealer_doc["short_name"],
                                    st=dealer_doc["st"], zip=dealer_doc["zip"])
        model_results.append(dealer_obj)
    return model_results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative



