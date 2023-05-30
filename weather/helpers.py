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
    params = {
        'access_key': settings.WEATHERSTACK_API["WEATHERSTACK_API_KEY"],
        'query': city_name
    }
    url = settings.WEATHERSTACK_API["WEATHERSTACK_API_URL"]
    weatherstack_response = requests.get(url, params)
    
    return weatherstack_response
