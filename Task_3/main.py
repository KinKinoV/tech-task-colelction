import requests
import json

# This functions makes requests to the OpenMeteo API using
# two required parameters and 6 optional parameters
def make_request(
        latitude: float, 
        longitude: float, 
        **kwargs
    ) -> requests.Response:
    # Base request URL
    url = "https://api.open-meteo.com/v1/forecast?"
    
    # List of values usable with `daily` and `hourly` parameters.
    # Description of listed vars is available at https://open-meteo.com/en/docs in Hourly Parameter Definition
    weather_vars = [
        "temperature_2m",
        "temperature_2m_max",
        "temperature_2m_min", 
        "apparent_temperature", 
        "cloud_cover", 
        "wind_speed_10m", 
        "precipation", 
        "visibility"]

    assert type(latitude) == float, "'latitude' variable must be a float value!"
    assert type(longitude) == float, "'longitude' variable must be a float value!"
    
    # Adding required parameters to the request
    url += f"latitude={latitude}&longitude={longitude}"
    
    # Parsing kwargs for possible request parameters and processing them
    hourly = kwargs.get('hourly', None)
    if hourly:
        url += "&hourly="
        assert type(hourly) == list, "'hourly' variable must be a list of strings!"
        for parameter in hourly:
            assert parameter in weather_vars, f"Parameter {parameter} of `hourly` variable is not allowed!"
            url += f"{parameter},"
    
    daily = kwargs.get('daily', None)
    if daily:
        url += "&daily="
        assert type(daily) == list, "'daily' variable must be a list of strings!"
        for parameter in daily:
            assert parameter in weather_vars, f"Parameter {parameter} of `daily` variable is not allowed!"
            url += f"{parameter},"
    
    timezone = kwargs.get('timezone', None)
    if timezone:
        assert type(timezone) == str, "'timezone must be a string!'"
        url += f"&timezone={timezone}"
    
    temperature_unit = kwargs.get('temperature_unit', None)
    if temperature_unit:
        assert type(temperature_unit) == str, "'temperature_unit' variable must be a string!"
        assert temperature_unit in ["celsius", "fahrenheit"], "Value of 'temperature_unit' must be 'celsius' or 'fahrenheit'!"
        url += f"&temperature_unit={temperature_unit}"
    
    past_days = kwargs.get('past_days', None)
    if past_days:
        assert type(past_days) == int, "'past_days' variable must be an int!"
        assert past_days > 0 and past_days <= 92, "Allowed range for 'past_days' is 0-92."
        url += f"&past_days={past_days}"
    
    forecast_days = kwargs.get('forecast_days', None)
    if forecast_days:
        assert type(forecast_days) == int, "'forecast_days' variable must be an int!"
        assert forecast_days > 0 and forecast_days <= 16, "Allowed range for 'forecast_days' is 0-16."
        url += f"&forecast_days={forecast_days}"

    return requests.get(url)

# Function that processes received data in the next ways:
# 1) Saves latitude, longtitude, timezone and units used
# 2) Counts average temperature for all mentioned days in the response
# 3) Returns a dictionary with recorded days, counted average temperature,
#    max temperature and minimal temperature for each day 
def process_data(data: dict) -> dict:
    
    day_avg_temp = 0.0
    times_added = 0

    # Copying needed information from the raw data
    result_dict = {
        "latitude": data['latitude'],
        "longtitude": data['longitude'],
        "timezone": data['timezone'],
        "units": {
            "time": data['hourly_units']['time'],
            "temperature": data['hourly_units']['temperature_2m']
        },
        "days": data['daily']['time'],
        "avg_tmp": [],
        "max_tmp": data['daily']['temperature_2m_max'],
        "min_tmp": data['daily']['temperature_2m_min']
    }

    # Counting average temperature for each day
    for temperature in data['hourly']['temperature_2m']:
        day_avg_temp += temperature
        times_added += 1

        if times_added % 24 == 0 and times_added != 0:
            result_dict['avg_tmp'].append(round(day_avg_temp/times_added, 2))
            day_avg_temp = 0
            times_added = 0

    # Checking that algorithm worked correctly
    assert len(result_dict['days']) == len(result_dict['avg_tmp']), f"Something went wrong, ammount of days in raw data and ammount of days calculated while processing doesn't match. Size of the result_dict['days'] is {len(result_dict['days'])}, size of the result_dict['avg_tmp'] is {len(result_dict['avg_tmp'])}"

    return result_dict

# This function saves processed data as json file
def save_json(raw_json: dict):
    ready_json = json.dumps(raw_json, indent=4)

    with open('processed.json', "w") as file:
        file.write(ready_json)

# This function is responsible for visualizing processed data
def make_graph(processed_data: dict):
    import matplotlib.pyplot as plt
    import numpy as np

    fig, ax = plt.subplots(figsize=(16, 8))
    ax.set_xlabel('Dates')
    ax.set_ylabel('Temperature, °C')
    ax.plot(processed_data['days'], processed_data['avg_tmp'], marker = 'o', linestyle = '-', label="average")
    ax.plot(processed_data['days'], processed_data['max_tmp'], marker = 'v', linestyle = '-', label="maximum")
    ax.plot(processed_data['days'], processed_data['min_tmp'], marker = 's', linestyle = '-', label="minimum")
    ax.legend()
    plt.xticks(ticks=range(len(processed_data['days'])), labels=processed_data['days'], rotation = 90)
    plt.yticks(ticks=range(40))
    plt.show()

if __name__ == "__main__":
    raw_data = make_request(
        latitude=50.4397908,  # Місцезнаходження Площі Українських Героїв
        longitude=30.5180406, # в Києві
        hourly=["temperature_2m", "apparent_temperature"],
        daily=["temperature_2m_max", "temperature_2m_min"],
        timezone = "EET",
        past_days = 14,
        forecast_days = 14
        ).json()

    processed_data = process_data(raw_data)

    save_json(processed_data)
    make_graph(processed_data)
    