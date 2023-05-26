from django.shortcuts import render

from .helpers import get_weather


def index(request):
    """View function for home page of site."""
    return render(request, 'index.html', context={})


def weather(request):
    """View function get weather html
    """
    weather_data = get_weather(
        request.POST.get('city_name', [''])[0]
    )
    try:
        weather_data.raise_for_status()
        response = weather_data.json()
    except Exception:
        response = {
            "success": False,
            "error": {
                "info": "Looks like our services are currently offline"
            }
        }
    if not response.get("success", True):
        context = response
    else:
        context = {
            "success": True,
            "temperature": response["current"]["temperature"],
            "name": response["location"]["name"],
            "country": response["location"]["country"],
            "weather_icons": response["current"]["weather_icons"][0],
            "hourlys": []
        }
        for forecast_date in response.get("forecast"):
            for hourly in response.get(
                "forecast", {}
            ).get(forecast_date, {}).get("hourly", []):
                """
                format time 
                Returns the time as a number in 24h format:
                0 = 12:00 AM
                100 = 1:00 AM
                200 = 2:00 AM
                ...
                1200 = 12:00 PM
                1300 = 1:00 PM
                etc.
                """
                time = hourly["time"]
                len_time = len(time)
                if len_time == 1:
                    time = "00:0" + time
                elif len_time == 2:
                    time = "00:" + time
                elif len_time == 3:
                    time = time[0] + ':' + time[1:]
                elif len_time == 4:
                    time = time[0:2] + ':' + time[2:]
                aux_dict = dict(
                    temperature=hourly["temperature"],
                    weather_icons=hourly["weather_icons"][0],
                    time=time
                )
                context["hourlys"].append(aux_dict)
    return render(request, 'weather/weather.html', context=context)