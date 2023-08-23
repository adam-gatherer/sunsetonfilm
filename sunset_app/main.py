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
    URL += f"&daily=sunset&timezone=GMT&forecast_days=14"
    r = requests.get(url=URL)
    data = r.json()
    sunset_list_index = 0
    fortnight_dict = {}
    for time in (data['daily']['time']):
        sunset_list = (data['daily']['sunset'])
        sunset_datetime = datetime.fromisoformat(sunset_list[sunset_list_index])
        fortnight_dict[sunset_datetime] = ""

        #
        # Gets the hours around sunset
        #
        hours_datetime = [datetime.fromisoformat(hour) for hour in (data['hourly']['time'])]
        lower_limit = sunset_datetime - timedelta(hours=2)
        upper_limit = sunset_datetime + timedelta(hours=1)
        indexes_of_interest = [
            h for h, hour in enumerate(hours_datetime)
            if hour > lower_limit and hour < upper_limit
        ]

        #
        # Creates list of weather data for each hour beore sunset
        #
        weather_list = [
            (data['hourly']['temperature_2m'][i],
            data['hourly']['precipitation_probability'][i],
            data['hourly']['visibility'][i],
            data['hourly']['windspeed_10m'][i],
            data['hourly']['windspeed_80m'][i],
            data['hourly']['soil_moisture_0_1cm'][i])
            for i in indexes_of_interest
        ]
        
        data_list = [
            avg_temp := 0,
            avg_precip := 0,
            avg_vis := 0,
            avg_wind10 := 0,
            avg_wind80 := 0,
            avg_moist := 0
        ]

        #
        # Get the avg weather data for the hours before sunset
        #
        for weather in weather_list:
            for c in range(0, 6):
                try:
                    data_list[c] += weather[c]
                except:
                    None
        avg_data_list = []
        for data_entry in data_list:
            if type(data_entry) == float:
                no_of_entries = len(weather_list)
                data_entry = round((data_entry / no_of_entries), 2)
            avg_data_list.append(data_entry)

        

        
        fortnight_dict[sunset_datetime] = avg_data_list
        sunset_list_index += 1
    
    return fortnight_dict


def find_good_dates(fortnight_dict: dict):
    for key, val in fortnight_dict.items():
        if (val[0] > 10) and (val[1] < 80):
            print(key)
    


lonlat = (-3.251163, 55.977057)
today = (date.today())
fortnight_dict = sunset_from_lonlat(lonlat, today)

#find_good_dates(fortnight_dict)