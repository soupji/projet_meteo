import requests, json, gzip, os
from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from io import BytesIO

def get_french_city_ids():
    '''
    Récupérer tous les ids des villes françaises, sert de référence pour lors de l'appel de l'API.

    @return: l'ensemble des villes françaises avec leurs ids
    '''
    response = requests.get('http://bulk.openweathermap.org/sample/city.list.json.gz') #récupérer le fichier de référence

    with gzip.open(BytesIO(response.content)) as f:
        data = json.load(f) #stocker les données sous forme de dictionnaire

    french_cities = [city['id'] for city in data if city['country'] == 'FR'] #stocker les données des villes françaises sous forme de liste

    return french_cities

app = Flask(__name__) #init de l'application flask

def get_weather_data(city_id):
    '''
    Requêter l'API pour récupérer les JSON de la ville passée en paramètre, via son id.

    @city_id: l'id de la ville à requêter

    @return: le JSON de la ville passée en paramètre
    '''
    url = f"http://api.openweathermap.org/data/2.5/weather?id={city_id}&appid=6998c4111e998e4901823c5e5a696b1f&units=metric" #appel API, penser à changer l'API key si run du code
    response = requests.get(url) #méthode GET pour récupérer les données

    return response.json()

mongo_uri = os.getenv("MONGO_URI", "mongodb://projet_meteo_mongodb:27017") #les identifiants de connexion de la base mongodb, paramètrer pour docker
mongo_client = MongoClient(mongo_uri) 
#client = MongoClient("mongodb://localhost:27017/")
db = mongo_client["meteo"] #nom de la base
collection = db["villes"] #nom de la connexion

def save_to_mongodb(city_data):
    '''
    Sauvegarder les données dans la base. 
    Une fonction avait été de base créer pour gérer différents cas de figure, acutellement la factorisation n'est pas nécessaire.

    @city_data: une ville sous forme de dict     
    '''
    collection.insert_one(city_data)

def run_mongo():
    '''
    Fonction permettant de déclencher tout le processus de sauvegarde des données dans mongodb.
    '''
    french_cities = get_french_city_ids() #on récupère les JSON de toutes les villes françaises

    for city_id in french_cities: #pour chaque ville
        weather_data = get_weather_data(city_id) #on récupère le JSON via l'API
        save_to_mongodb(weather_data) #on sauvegarde les données dans la base mongodb

@app.route('/') #homepage
def home():
    return "Open Weather API Data"

@app.route('/weather/<int:city_id>') #visualiser le JSON d'une ville
def get_city_weather(city_id):
    '''
    Route flask pour visualiser le JSON de la ville passée en paramètre, via son id.

    @city_id: l'id de la ville à requêter (à retrouver dans le fichier de référence)

    @return: le JSON de la ville passée en paramètre
    '''
    weather_data = get_weather_data(city_id)
    
    return jsonify(weather_data)

run = input("Souhaitez-vous interroger l'API ou sauvegarder les données dans MongoDB? (y/n): ")

if run == 'y':
    run_mongo() #lancement du processus de sauvegarde des données dans mongodb
else:
    pass #utilisation des routes flask

if __name__ == '__main__':
    app.run( )