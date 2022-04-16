import requests
import json
# import related models here
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
# auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        if 'api_key' in kwargs:
            response = requests.get(url, headers={'Content-Type': 'application/json'}, data=kwargs['params'], auth=HTTPBasicAuth('apikey', kwargs['api_key']))
        else:
            response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs)
        
    except:
        # If any error occurs
        print("Network exception occurred")
    
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    try:
        response = requests.post(url, params=kwargs, json=json_payload)
    except:
        # If any error occurs
        print("Network exception occurred")
    
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["docs"]
        # For each dealer object
        for dealer_doc in dealers:
            # Get its content in `doc` object
            # dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(
                id=dealer_doc["id"], 
                city=dealer_doc["city"],
                state=dealer_doc["state"],
                st=dealer_doc["st"],
                address=dealer_doc["address"],
                zip=dealer_doc["zip"],
                lat=dealer_doc["lat"], 
                long=dealer_doc["long"],
                full_name=dealer_doc["full_name"],
                short_name=dealer_doc["short_name"],
            )
            results.append(dealer_obj)

    return results


# Create a get_dealer_by_id method to get a specific dealer
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealer_by_id(url, **kwargs):
    results = []
    print (kwargs)
    # Call get_request with a URL parameter
    json_result = get_request(url, dealership=kwargs['dealer_id'])
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["docs"]
        # For each dealer object
        for dealer_doc in dealers:
            # Get its content in `doc` object
            # dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(
                id=dealer_doc["id"], 
                city=dealer_doc["city"],
                state=dealer_doc["state"],
                st=dealer_doc["st"],
                address=dealer_doc["address"],
                zip=dealer_doc["zip"],
                lat=dealer_doc["lat"], 
                long=dealer_doc["long"],
                full_name=dealer_doc["full_name"],
                short_name=dealer_doc["short_name"],
            )
            results.append(dealer_obj)

    return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, dealership=kwargs['dealer_id'])
    if json_result:
        # Get the row list in JSON as dealers
        print (json_result)
        reviews = json_result["revs"]
        # For each dealer object
        for review_doc in reviews:
            # Create a DealerReview object with values in `doc` object
            review_obj = DealerReview(
                id=review_doc["id"], 
                name=review_doc["name"],
                dealership=review_doc["dealership"],
                review=review_doc["review"],
                purchase=review_doc["purchase"],
                purchase_date=review_doc["purchase_date"],
                car_make=review_doc["car_make"], 
                car_model=review_doc["car_model"],
                car_year=review_doc["car_year"],
                sentiment=analyze_review_sentiments(review_doc["review"])
            )
            results.append(review_obj)

    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(text):
    url = "https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/f44fc8e9-01c1-415d-8337-8431562bd6f5"

    params = dict()
    params["text"] = text
    params["version"] = "2022-04-07"
    # params["features"] = "{ 'categories': { 'limit': 3 }"
    # params["api_key"] = "LpCAomx-5h6kk6KazkDgz5t0M2Gpe-OEHEsnH8WrKeNF"
    
    response = get_request(url, params=params, api_key="LpCAomx-5h6kk6KazkDgz5t0M2Gpe-OEHEsnH8WrKeNF")
    print (response)
    return response
