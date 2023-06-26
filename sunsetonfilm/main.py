# sunsetonfilm/main.py

import requests

lat = float(55.97706)
lng = float(-3.25116)
date = "2023-06-23"
url = "https://api.sunrise-sunset.org/json"

parameters = {
    'lat': lat,
    'lng': lng,
    'date': date
}

r = requests.get(url = url, params = parameters)
data = r.json()

sunset = data['results']['sunset']

print(sunset)