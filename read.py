import json
import requests
import os
from geopy import distance
import folium
from dotenv import load_dotenv


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
    return lat, lon


def main():
    load_dotenv()
    api = os.getenv('APIKEY')
    with open("coffee.json", "r", encoding="CP1251") as my_file:
        coffee_content = my_file.read()
    coffees = json.loads(coffee_content)
    apikey = api
    place = input()
    coords = fetch_coordinates(apikey, place)

    coffeeshops = []

    for coffee in coffees:
        coffee_title = coffee['Name']
        coffee_coordinates1 = coffee['Latitude_WGS84']
        coffee_coordinates2 = coffee['Longitude_WGS84']
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
    first_coffeeshops = sorted(coffeeshops, key=get_distance)[:5]

    m = folium.Map(location=coords)

    for shop in first_coffeeshops:
        folium.Marker(
            location=[shop['latitude'], shop['longitude']],
            tooltip="Click me!",
            popup=[shop['title']],
            icon=folium.Icon(icon="cloud"),
        ).add_to(m)
    m.save("index.html")


if __name__ == "__main__":
    main()
