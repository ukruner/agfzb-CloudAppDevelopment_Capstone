import requests
import json
from .models import CarDealer, CarReview
from requests.auth import HTTPBasicAuth
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 \
    import Features, SentimentOptions, EntitiesOptions, KeywordsOptions



def get_request(url, auth=None, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # if api_key:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'}, auth=HTTPBasicAuth('apikey', 'h6OLXbfGGoKT14A9zpZsPIupGnKUeBaas_EqTfHPNOhn'),
                                    params=kwargs)
        # else:
        #     response = requests.get(url, headers={'Content-Type': 'application/json'},
        #                             params=kwargs)

    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            print("Dealer",dealer_doc)
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

def get_reviews_from_cf(url, **kwargs):
    results = []
    keylist = ['dealership', 'name', 'id', 'review', 'purchase', 'purchase_date', 'car_make', 'car_model', 'car_year']
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        reviews = json_result
        print(reviews)
        # For each dealer object
        for review in reviews:
            for k in keylist:
                if k not in review.keys():
                    review[k]=''
            # Get its content in `doc` object
            review_obj = review
            print("Review", review_obj)
            # Create a CarDealer object with values in `doc` object
            review_new = CarReview(dealership=review_obj['dealership'],
            name=review_obj['name'],
            id=review_obj['id'],
            review=review_obj['review'],
            purchase=review_obj['purchase'],
            purchase_date=review_obj['purchase_date'],
            car_make=review_obj['car_make'],
            car_model=review_obj['car_model'],
            car_year=review_obj['car_year'],
            sentiment=analyze_review_sentiments(review_obj['review']))
            results.append(review_new)

    return results

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)

def post_request(url, json_payload, **kwargs):
    required_fields = ['id', 'name', 'dealership', 'review', 'purchase', 'time']
    if not json_payload:
        return HttpResponseBadRequest("JSON data missing")

    # Validate that the required fields are present in the review data
    else:
        for field in required_fields:
            if field not in json_payload.keys():
                return HttpResponseBadRequest(f"{field} is a required field, and it is missing")
        requests.post(url, params=kwargs, json=json_payload)


    # Save the review data as a new document in the Cloudant database

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative


def analyze_review_sentiments(dealerreview):
    authenticator = IAMAuthenticator('h6OLXbfGGoKT14A9zpZsPIupGnKUeBaas_EqTfHPNOhn')
    natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2022-04-07',
    authenticator=authenticator)

    natural_language_understanding.set_service_url('https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/5cab2d96-30be-48f9-9c7f-3f040d30a079')
    if len(dealerreview) < 20:
        return {"error": "Text is too short to analyze"}
    else:
        response = natural_language_understanding.analyze(
        text=dealerreview,
        features=Features(
            entities=EntitiesOptions(emotion=True, sentiment=True, limit=2),
            keywords=KeywordsOptions(emotion=True, sentiment=True,
                                    limit=2))).get_result()

        print(json.dumps(response, indent=2))
        sentiment_response = response['keywords'][0]['sentiment']['label']
        return sentiment_response







