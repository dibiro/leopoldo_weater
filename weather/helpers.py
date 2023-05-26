from django.conf import settings
import requests


def get_weather(city_name: str):
    """ This function connects to the weatherstack api 
    passing as a parameter the name of the city to consult


    Parameters
    ----------
    city_name str
        name of city for query.

    Return
    ------
    requests
        resquests intances
    """
    url = (
        f'{settings.WEATHERSTACK_API["WEATHERSTACK_API_URL"]}'
        f'?access_key={settings.WEATHERSTACK_API["WEATHERSTACK_API_KEY"]}'
        f'&query={city_name}&forecast_days=1&hourly=1'
    )
    weatherstack_response = requests.get(url)
    
    return weatherstack_response
