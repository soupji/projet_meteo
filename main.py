import requests, json, gzip
from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from io import BytesIO

def get_french_city_ids():
    '''response = requests.get('http://bulk.openweathermap.org/sample/city.list.json.gz')

    with gzip.open(response.content) as f:
        data = json.load(f)

    french_cities = [city['id'] for city in data if city['country'] == 'FR']

    return french_cities'''

    response = requests.get('http://bulk.openweathermap.org/sample/city.list.json.gz')

    with gzip.open(BytesIO(response.content)) as f:
        data = json.load(f)

    french_cities = [city['id'] for city in data if city['country'] == 'FR']

    return french_cities

app = Flask(__name__)

def get_weather_data(city_id):
    url = f"http://api.openweathermap.org/data/2.5/weather?id={city_id}&appid=6998c4111e998e4901823c5e5a696b1f&units=metric"
    response = requests.get(url)

    return response.json()

client = MongoClient("mongodb://localhost:27017/")
db = client["meteo"]
collection = db["villes"]

def save_to_mongodb(city_data):
    collection.insert_one(city_data)

def run_mongo():
    french_cities = get_french_city_ids()

    for city_id in french_cities:
        weather_data = get_weather_data(city_id)
        save_to_mongodb(weather_data)

@app.route('/')
def home():
    return "Open Weather API Data"

@app.route('/weather/<int:city_id>')
def get_city_weather(city_id):
    weather_data = get_weather_data(city_id)
    
    return jsonify(weather_data)

run = input("Souhaitez-vous interroger l'API ou sauvegarder les données dans MongoDB? (y/n): ")

if run == 'y':
    run_mongo()
else:
    pass

if __name__ == '__main__':
    app.run( )