from .api_interface import ApiInterface
from .url_search_params import URLSearchParams

class NewsApi(ApiInterface):

    API_KEY_FNAME = "./mybase/apis/news_api_key.env"
    API_URL = "https://newsapi.org/v2/everything"

    def __init__(self):
        with open(NewsApi.API_KEY_FNAME, "r") as f:
            self.apiKey = f.read().strip()

    def getUrl(self, json):
        params = json
        params["apiKey"] = self.apiKey
        return URLSearchParams.setSearchParams(NewsApi.API_URL, params)
