import requests
import time
import sys
import logging
from http_build_query import http_build_query


logger = logging.getLogger('bproxy')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stderr))


class Error(Exception):
    pass


URL = 'http://api.best-proxies.ru/feeds/proxylist.{format}'


class Api(object):

    '''
    Usage:
        client = Api('apikey', debug=False)
        res = client.call(format='csv', limit=2, includeType=1, country='ru,us')
    '''
    def __init__(self, api_key, debug=False):
        self.API_KEY = api_key

        self.last_request = None
        self.default_format = 'txt'

        if debug:
            self.level = logging.INFO
        else:
            self.level = logging.DEBUG

    def call(self, **kwargs):
        format = kwargs.get('format', self.default_format)

        try:
            del kwargs['format']
        except KeyError:
            pass

        _params = {
            'key': self.API_KEY,
        }

        _params.update(kwargs or {})

        url = URL.format(format=format) + '?' + http_build_query(_params)

        request = Request(url)

        return self.send_request(request)

    def send_request(self, request):

        if self.last_request:
            time_delta = time.time() - self.last_request.timestamp
            if time_delta < 5:
                time.sleep(5 - time_delta + 1)

        self.last_request = request

        self.log('Executing %s' % request.url)
        start = time.time()

        request.timestamp = time.time()
        http_response = requests.get(request.url)

        complete_time = time.time() - start
        self.log('Received %s in %.2fms: %s' % (http_response.status_code, complete_time * 1000, http_response.text))

        return http_response.text

    def log(self, *args, **kwargs):
        logger.log(self.level, *args, **kwargs)


class Request(object):

    def __init__(self, url):
        self.url = url

        self.timestamp = None


# class Response(object):
#
#     def __init__(self, request):
#         pass
