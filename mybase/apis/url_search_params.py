# From: https://stackoverflow.com/questions/2506379/add-params-to-given-url-in-python
import urllib.parse as urlp
from urllib.parse import urlencode

class URLSearchParams:
    URL_PARTS_PARAMS_IX = 4
    @staticmethod
    def setSearchParams(url, params):
        url_parts = list(urlp.urlparse(url))
        url_parts[URLSearchParams.URL_PARTS_PARAMS_IX] = urlencode(params)
        return urlp.urlunparse(url_parts)