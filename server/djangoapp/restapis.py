import requests
import json
# import related models here
from requests.auth import HTTPBasicAuth
from .models import CarDealer, DealerReview


api_key = "PBUzim7grD8wBmewfwf7Y14ih6PKq69c-Pft7EyefVNT"
nlu_url = "https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/11b5b488-924a-43c9-b20b-f276659fd4b2"

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list

def get_dealers_by_id_from_cf(url, **kwargs):
    
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url,id=kwargs["dealer_id"])
    #print(json_result[0])
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        #print(dealers[0])
        # For each dealer object
        for dealer_doc in dealers:
            # Get its content in `doc` object
            
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealers_from_cf(url, **kwargs):
    
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    #print(json_result[0])
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        #print(dealers[0])
        # For each dealer object
        for dealer_doc in dealers:
            # Get its content in `doc` object
            print(dealer_doc)
            
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])

            
            results.append(dealer_obj)

    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative

def get_dealers_reviews_from_cf(url, **kwargs):
    reviews = []
    # Call get_request with a URL parameter
    json_result = get_request(url,id=kwargs["dealer_id"])
    print(json_result)
    if json_result:
        # Get the row list in JSON as dealers
        reviews_list = json_result
        #print(reviews)
        # For each dealer object
        for review_doc in reviews_list:
            # Get its content in `doc` object
            
            # Create a CarDealer object with values in `doc` object
            #print(review_doc)
            
            
            review_obj = DealerReview(dealership=review_doc["dealership"],name=review_doc["name"],purchase=review_doc["purchase"], review=review_doc["review"],purchase_date=review_doc["purchase_date"], car_make=review_doc["car_make"], car_model=review_doc["car_model"], car_year=review_doc["car_year"],sentiment= "",id=review_doc["id"])
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            print(review_obj.sentiment)
            reviews.append(review_obj)

    return reviews

def analyze_review_sentiments(dealerreview):
    body = {"text": dealerreview, "features": {"sentiment": {"document": True}}}
    #print(dealerreview)
    response = requests.post(
        nlu_url + "/v1/analyze?version=2019-07-12",
        headers={"Content-Type": "application/json"},
        json=body,  # Use json parameter for automatic conversion
        auth=HTTPBasicAuth("apikey", api_key),
    )

    # Check if request was successful
    if response.status_code == 200:
        sentiment = response.json()["sentiment"]["document"]["label"]
        return sentiment
    return "N/A"
    

 

