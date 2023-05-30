from django.shortcuts import render

from .helpers import get_weather


def index(request):
    """View function for home page of site."""
    return render(request, 'index.html', context={})


def weather(request):
    """View function get weather html
    """
    weather_data = get_weather(
        request.POST.get('city_name', '')
    )
    try:
        weather_data.raise_for_status()
        json_response = weather_data.json()
    except Exception:
        json_response = {
            "success": False,
            "error": {
                "info": "Looks like our services are currently offline"
            }
        }
    if not json_response.get("success", True):
        context = json_response
    else:
        context = {
            "success": True,
            "temperature": json_response["current"]["temperature"],
            "name": json_response["location"]["name"],
            "country": json_response["location"]["country"],
            "weather_icons": json_response["current"]["weather_icons"][0],
            "hourlys": []
        }
    return render(request, 'weather/weather.html', context=context)