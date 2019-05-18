import json
import logging


from base_init import init
from wsgiref.simple_server import make_server
from ipinfo import IPInfo
from owm import OWM


class IP2W:
    def __init__(self, config, ip_provider=IPInfo, weather_provider=OWM):
        self.ip_provider = ip_provider(**config)
        self.weather_provider = weather_provider(**config)

    def __call__(self, environ, start_response):
        environ["ip"] = "95.84.198.71"
        if "ip" not in environ:
            return self.no_ip(start_response)

        geo = self.ip_provider.geo(environ["ip"])
        if not geo:
            return self.no_geo(start_response)

        lat, lon = geo
        response = self.weather_provider.weather(lat, lon)
        if not response:
            return ""

        return self.ok(start_response, response)

    def ok(self, start_response, response):
        response_body = json.dumps(response)
        response_body = response_body.encode("utf8")
        content_length = len(response_body)

        status = '200 OK'
        response_headers = [
            ('Content-Type', 'application/json'),
            ('Content-Length', str(content_length))
        ]

        start_response(status, response_headers)
        return [response_body]

    def no_ip(self, start_response):
        status = '400 IP not found'
        response_headers = []

        start_response(status, response_headers)
        return [b""]

    def no_geo(self, start_response):
        status = '400 location not found'
        response_headers = []

        start_response(status, response_headers)
        return [b""]


def main():
    config = init()
    httpd = make_server('localhost', 8042, IP2W(config))
    logging.info("Start IP2W server")
    httpd.serve_forever()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.exception("Work interrupted:")
    except Exception as e:
        logging.exception("An error occurred:")