import requests

import config


class ApiKeyError(Exception):
    ...


class OrganicResult:
    def to_dict(self) -> dict:
        return self.__kwargs

    def __eq__(self, other: 'OrganicResult'):
        return self.domain == other.domain

    def __repr__(self):
        res = f'{type(self).__name__}(domain={self.domain})'
        return res

    def __init__(self, **kwargs):
        self.__kwargs = kwargs
        self.url: str = kwargs['url']
        self.displayed_url: str = kwargs['displayed_url']
        self.description: str = kwargs['description']
        self.position: int = kwargs['position']
        self.title: str = kwargs['title']
        self.domain: str = kwargs['domain']
        self.sitelinks: list = kwargs['sitelinks']
        self.rich_snippet: dict = kwargs['rich_snippet']
        self.date = kwargs['date']
        self.date_utc = kwargs['date_utc']


class ScrapingObject:
    organic_results: list[OrganicResult]

    def __init__(self, *args, **kwargs):
        self.organic_results = [
            OrganicResult(**i) for i in kwargs.get('organic_results')
        ]
        self.__args = args
        self.__kwargs = kwargs


def send_request(params: dict) -> ScrapingObject:
    params['api_key'] = config.SCRAPINGBEE_APIKEY
    response = requests.get(
        url="https://app.scrapingbee.com/api/v1/store/google",
        params=params,

    )
    error_message = response.json().get('message')
    if not error_message:
        return ScrapingObject(**response.json())
    else:
        if 'Invalid api key' in error_message:
            raise ApiKeyError(response.json())
