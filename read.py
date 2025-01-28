import json
import requests
from geopy import distance
from pprint import pprint
import folium


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
    with open("coffee.json", "r", encoding="CP1251") as my_file:
        coffee_content = my_file.read()
    coffees = json.loads(coffee_content)
    apikey='306ca3f2-7d2b-4867-af78-2147178d15c3'
    place = input()
    coords = fetch_coordinates(apikey, place)

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
    first_coffeeshops = sorted(coffeeshops, key=get_distance)[:5]

    m=folium.Map(location=coords)
    folium.Marker(
        location=[55.7557913293247580, 37.6215290000000020],
        tooltip="Click me!",
        popup="Кофе Хауз",
        icon=folium.Icon(icon="cloud"),
    ).add_to(m)
    folium.Marker(
        location=[55.7544881949865920, 37.6094491636510710],
        tooltip="Click me!",
        popup="Cafetera",
        icon=folium.Icon(icon="cloud"),
    ).add_to(m)
    folium.Marker(
        location=[55.7471397548410150, 37.6079790000000000],
        tooltip="Click me!",
        popup="Fine кофе",
        icon=folium.Icon(icon="cloud"),
    ).add_to(m)
    folium.Marker(
        location=[55.7471037302211770, 37.6076198783218700],
        tooltip="Click me!",
        popup="Costa coffee",
        icon=folium.Icon(icon="cloud"),
    ).add_to(m)
    folium.Marker(
        location=[55.7537403409148600, 37.6055678397103890],
        tooltip="Click me!",
        popup="КОФЕПОРТ",
        icon=folium.Icon(icon="cloud"),
    ).add_to(m)
    m.save("index.html")

if __name__=="__main__":
    main()
    
