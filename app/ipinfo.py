import requests


class IPInfo:
    def __init__(self, ipinfo_url=None, *args, **kwargs):
        if not ipinfo_url:
            raise ValueError("IPInfo url not found")
        self.url = ipinfo_url

    def geo(self, ip):
        url = self.url
        response = requests.get(url.format(ip=ip)).json()
        return response["loc"].split(",")