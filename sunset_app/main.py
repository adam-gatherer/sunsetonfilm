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
    URL += f"&hourly=temperature_2m,precipitation_probability,visibility,windspeed_10m,windspeed_80m,soil_moisture_0_1cm"
    URL += f"&daily=sunset&timezone=GMT&forecast_days=2"
    r = requests.get(url=URL)
    data = r.json()
    i = 0
    fortnight_dict = {}
   
    for time in (data['daily']['time']):
        sunsetlist = (data['daily']['sunset'])
        sunset_datetime = datetime.fromisoformat(sunsetlist[i])
        fortnight_dict[sunset_datetime] = ""

        hours_datetime = [datetime.fromisoformat(hour) for hour in (data['hourly']['time'])]

        lower_limit = sunset_datetime - timedelta(hours=2)
        upper_limit = sunset_datetime + timedelta(hours=1)

        print(sunset_datetime)

        indexes_of_interest = [
            i for i, hour in enumerate(hours_datetime)
            if hour > lower_limit and hour < upper_limit
        ]

        weather = [
            (data['hourly']['temperature_2m'][i],
            data['hourly']['precipitation_probability'][i],
            data['hourly']['visibility'][i],
            data['hourly']['windspeed_10m'][i],
            data['hourly']['windspeed_80m'][i],
            data['hourly']['soil_moisture_0_1cm'][i])
            for i in indexes_of_interest
        ]
        print(weather) 
     #print(fortnight_dict)       

      
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