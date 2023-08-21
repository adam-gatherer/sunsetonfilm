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

       
        weather_list = [
            (data['hourly']['time'][i],
            data['hourly']['temperature_2m'][i],
            data['hourly']['precipitation_probability'][i],
            data['hourly']['visibility'][i],
            data['hourly']['windspeed_10m'][i],
            data['hourly']['windspeed_80m'][i],
            data['hourly']['soil_moisture_0_1cm'][i])
            for i in indexes_of_interest
        ]

        
        #avg_temp = 0
        #avg_precip = 0
        #avg_vis = 0
        #avg_wind10 = 0
        #avg_wind80 = 0
        #avg_moist = 0

        data_list = [
            data['hourly']['time'][i],
            avg_temp := 0,
            avg_precip := 0,
            avg_vis := 0,
            avg_wind10 := 0,
            avg_wind80 := 0,
            avg_moist := 0
        ]
        
        x = 1
        d = 0
        for weather in weather_list:
            #data_list[0] += weather[1]
            #data_list[1] += weather[2]
            #data_list[2] += weather[3]
            #data_list[3] += weather[4]
            #data_list[4] += weather[5]
            #data_list[5] += weather[6]
            for c in range(1, 7):
                data_list[c] += weather[c]
                #data_list[c] = round(data_list[c], 2)

        for data_entry in data_list:
            if type(data_entry) == float:
                data_entry = data_entry / len(weather_list)


        print(data_list)



lonlat = (-3.251163, 55.977057)
today = (date.today())
sunset_from_lonlat(lonlat, today)