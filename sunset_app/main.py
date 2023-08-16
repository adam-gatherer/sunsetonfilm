import requests
import json
from datetime import timedelta, date, datetime

def lonlat_from_postcode(postcode: str) -> tuple[float, float]:
    URL = "https://api.postcodes.io/postcodes/" + postcode
    r = requests.get(url=URL)
    data = r.json()
    if r.status_code == 200:
        long = data['result']['longitude']
        lat = data['result']['latitude']
        return float(long), float(lat)

def sunset_from_lonlat(lonlat: tuple, today) -> dict:
    lon = lonlat[0]
    lat = lonlat[1]
        
    # https://api.sunrisesunset.io/json?lat=38.907192&lng=-77.036873&timezone=UTC&date=1990-05-22
    # https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41
    # &hourly=temperature_2m,precipitation_probability,visibility,windspeed_10m,soil_moisture_0_1cm
    # &daily=sunset&timezone=GMT&forecast_days=14
    # URL = f"https://api.sunrisesunset.io/json?lat={lat}&lng={lon}&date={date}"

    URL = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
    URL += f"&hourly=temperature_2m,precipitation_probability,visibility,windspeed_10m,soil_moisture_0_1cm"
    URL += f"&daily=sunset&timezone=GMT&forecast_days=2"
    r = requests.get(url=URL)
    data = r.json()
    #sunset = (data['results']['sunset'])
    i = 0
    fortnight = {}
    #print(data['daily']['time'])
    
    for time in (data['daily']['time']):

        sunsetlist = (data['daily']['sunset'])
        dict_key = (sunsetlist[i]).replace("T", "")
        fortnight[dict_key] = ""
        #sunset = f"{data['daily']['sunset'][i]}"
        i += 1
    for key, val in fortnight.items():
        date = datetime.strptime(key, "%Y-%m-%d%H:%M")
        x = 0
        for time in (data['hourly']['time']):
            time = time.replace("T", "")
            time = datetime.strptime(time, "%Y-%m-%d%H:%M")
            if (time.day == date.day) and (time.hour in range ((date.hour) -2, (date.hour +1))):
                fortnight[key] = (
                    str(date),
                    data['hourly']['temperature_2m'][x],
                    data['hourly']['precipitation_probability'][x],
                    data['hourly']['visibility'][x],
                    data['hourly']['windspeed_10m'][x],
                    data['hourly']['soil_moisture_0_1cm'][x]
                )       
            x += 1

        for key, val in fortnight.items():
            print(f'{key} - {val}')
        
    #for item in (data['hourly']):
    #   print(item[0])

lonlat = (-3.251163, 55.977057)

today = (date.today())

sunset_from_lonlat(lonlat, today)

#time1 = "2023-08-16T19:48"
#time1 = time1.replace("T", "")
#time1 = datetime.strptime(time1, "%Y-%m-%d%H:%M")
#timelist = ["2023-08-16T16:00", "2023-08-16T17:00", "2023-08-16T18:00", "2023-08-16T19:00", "2023-08-16T20:00", "2023-08-16T21:00", "2023-08-16T22:00"]

#for time in timelist:
#    time = time.replace("T", "")
#    time = datetime.strptime(time, "%Y-%m-%d%H:%M")
#    if time.hour in range((time1.hour)-2,time1.hour+1) :
#        print(time)    