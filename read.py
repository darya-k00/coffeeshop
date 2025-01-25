import json
import requests
from geopy import distance
from pprint import pprint

with open("coffee.json", "r", encoding="CP1251") as my_file:
	coffee_content = my_file.read()
coffees = json.loads(coffee_content)

def fetch_coordinates(apikey, address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": apikey,
        "format": "json",
    })
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lon, lat

apikey='306ca3f2-7d2b-4867-af78-2147178d15c3'
print("Где вы находитесь?")
place = input()
coords = fetch_coordinates(apikey, place)
print("Ваши координаты:", coords)

coffeeshops = []

for coffee in coffees:
    coffee_title=coffee['Name']
    coffee_coordinates1=coffee['Latitude_WGS84']
    coffee_coordinates2=coffee['Longitude_WGS84']
    coffee_coords = (coffee_coordinates1, coffee_coordinates2)
    dist = distance.distance(coords, coffee_coords).km
    coffeeshops.append({
        'title': coffee_title,
        'distance': dist,
        'latitude': coffee_coordinates1,
        'longitude': coffee_coordinates2
    })
def get_distance(coffeeshop):
    return coffeeshop['distance']  
coffeemin = min(coffeeshops, key=get_distance )
pprint(coffeemin)
