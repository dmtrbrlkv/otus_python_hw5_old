import requests


class OWM:
    def __init__(self, owm_url=None, owm_token=None, *args, **kwargs):
        if not owm_url:
            raise ValueError("OWM url not found")
        if not owm_token:
            raise ValueError("OWM token not found")

        self.url = owm_url
        self.token = owm_token

    def weather(self, lat, lon):
        url = self.url
        response = requests.get(url.format(lat=lat, lon=lon, token=self.token)).json()

        weather = {
            "city": response["name"],
            "temp": response["main"]["temp"],
            "conditions": response["weather"][0]["main"]
        }

        return weather
