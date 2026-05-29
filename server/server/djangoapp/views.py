from django.http import JsonResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth import logout
import logging
import json
from django.views.decorators.csrf import csrf_exempt

# IMPORTATIONS SUPPLÉMENTAIRES
from .models import CarMake, CarModel
from .populate import initiate
# Ajout de post_review pour l'envoi des avis
from .restapis import get_request, analyze_review_sentiments, post_review  

# Get an instance of a logger
logger = logging.getLogger(__name__)

@csrf_exempt
def registration(request):
    context = {}
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']
    username_exist = False
    email_exist = False
    try:
        User.objects.get(username=username)
        username_exist = True
    except:
        logger.debug("{} is new user".format(username))

    if not username_exist:
        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password, email=email)
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
        return JsonResponse(data)
    else:
        data = {"userName": username, "error": "Already Registered"}
        return JsonResponse(data)


def login_user(request):
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)

def logout_request(request):
    logout(request)
    data = {"userName": ""}
    return JsonResponse(data)

# Méthode pour obtenir la liste des voitures
def get_cars(request):
    count = CarMake.objects.filter().count()
    print(count)
    if(count == 0):
        initiate()
    car_models = CarModel.objects.select_related('car_make')
    cars = []
    for car_model in car_models:
        cars.append({"CarModel": car_model.name, "CarMake": car_model.car_make.name})
    return JsonResponse({"CarModels": cars})


# --------------------------------------------------------------------------
# VUES POUR LES CONCESSIONNAIRES AND LES CRITIQUES
# --------------------------------------------------------------------------

# Vue pour obtenir tous les concessionnaires (ou par État si spécifié)
def get_dealerships(request, state="All"):
    if(state == "All"):
        endpoint = "/fetchDealers"
    else:
        endpoint = "/fetchDealers/" + state
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})


# Vue pour obtenir les détails d'un concessionnaire spécifique via son ID
def get_dealer_details(request, dealer_id):
    if(dealer_id):
        endpoint = "/fetchDealer/" + str(dealer_id)
        dealer = get_request(endpoint)
        return JsonResponse({"status": 200, "dealer": dealer})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})


# Vue pour obtenir les critiques d'un concessionnaire et analyser leur sentiment
def get_dealer_reviews(request, dealer_id):
    if(dealer_id):
        endpoint = "/fetchReviews/dealer/" + str(dealer_id)
        reviews = get_request(endpoint)
        for review_detail in reviews:
            # Appel au microservice d'analyse de sentiment
            response = analyze_review_sentiments(review_detail['review'])
            print(response)
            review_detail['sentiment'] = response['sentiment']
        return JsonResponse({"status": 200, "reviews": reviews})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})


# Vue pour ajouter une critique (Review) sur un concessionnaire
@csrf_exempt
def add_review(request):
    if (request.user.is_authenticated == False):
        data = json.loads(request.body)
        try:
            response = post_review(data)
            return JsonResponse({"status": 200})
        except Exception as err:
            return JsonResponse({"status": 401, "message": "Error in posting review"})
    else:
        data = json.loads(request.body)
        try:
            response = post_review(data)
            return JsonResponse({"status": 200})
        except Exception as err:
            return JsonResponse({"status": 401, "message": "Error in posting review"})