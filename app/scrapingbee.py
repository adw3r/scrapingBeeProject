from datetime import datetime

import requests

from app import config
from app.database import ToDict


class ApiKeyError(Exception):
    ...


class SearchingQuery(ToDict):
    search: str
    page: int
    api_key: str
    add_html: bool
    extra_params: str
    country_code: str
    language: str
    nb_results: int
    device: str
    search_type: str

    def __init__(self,
                 search: str,
                 page: int = 1,
                 api_key: str = config.SCRAPINGBEE_APIKEY,
                 add_html: bool = False,
                 extra_params: str = '',
                 country_code: str = 'us',
                 language: str = 'en',
                 nb_results: int = 100,
                 device: str = 'desktop',
                 search_type: str = 'classic',
                 ):
        self.search = search
        self.page = page
        self.api_key = api_key
        if not self.api_key:
            raise ApiKeyError('ScrapingBee ApiKey can`t be empty!')
        self.add_html = add_html
        self.extra_params = extra_params
        self.country_code = country_code
        self.language = language
        self.nb_results = nb_results
        self.device = device
        self.search_type = search_type

    def to_dict(self) -> dict:
        return {
            'search': self.search,
            'page': self.page,
            'api_key': self.api_key,
            'add_html': self.add_html,
            'extra_params': self.extra_params,
            'country_code': self.country_code,
            'language': self.language,
            'nb_results': self.nb_results,
            'device': self.device,
            'search_type': self.search_type
        }


class OrganicResult(ToDict):
    url: str
    displayed_url: str
    description: str
    position: int
    title: str
    domain: str
    sitelinks: list
    rich_snippet: dict
    date: str
    date_utc: str

    def to_dict(self) -> dict:
        return {
            'url': self.url,
            'displayed_url': self.displayed_url,
            'description': self.description,
            'position': self.position,
            'title': self.title,
            'domain': self.domain,
            'sitelinks': self.sitelinks,
            'rich_snippet': self.rich_snippet,
            'date': self.date,
            'date_utc': self.date_utc
        }

    def __eq__(self, other: 'OrganicResult'):
        return self.domain == other.domain

    def __repr__(self):
        res = f'{type(self).__name__}(domain={self.domain})'
        return res

    def __init__(self,
                 url: str,
                 displayed_url: str,
                 description: str,
                 position: int,
                 title: str,
                 domain: str,
                 sitelinks: list,
                 rich_snippet: dict,
                 date: str,
                 date_utc: str
                 ):
        self.url: str = url
        self.displayed_url: str = displayed_url
        self.description: str = description
        self.position: int = position
        self.title: str = title
        self.domain: str = domain
        self.sitelinks: list = sitelinks
        self.rich_snippet: dict = rich_snippet
        self.date: str = date
        self.date_utc: str = date_utc


class ScrapingObject(ToDict):
    searching_query: SearchingQuery
    created_at: datetime = datetime.now()
    organic_results: list[OrganicResult]
    status: str = 'not viewed'
    organic_results: list
    meta_data: dict
    local_results: list
    top_ads: list
    bottom_ads: list
    related_queries: list
    questions: list
    top_stories: list
    news_results: list
    knowledge_graph: dict
    related_searches: list

    def to_dict(self) -> dict:
        return {
            'organic_results': [organic_res.to_dict() for organic_res in self.organic_results],
            'created_at': self.created_at.isoformat(),
            'searching_query': self.searching_query.to_dict(),
            'meta_data': self.meta_data,
            'local_results': self.local_results,
            'top_ads': self.top_ads,
            'bottom_ads': self.bottom_ads,
            'related_queries': self.related_queries,
            'questions': self.questions,
            'top_stories': self.top_stories,
            'news_results': self.news_results,
            'knowledge_graph': self.knowledge_graph,
            'related_searches': self.related_searches,
            'status': self.status,
        }

    def __init__(self,
                 searching_query: SearchingQuery,
                 organic_results: list,
                 meta_data: dict,
                 local_results: list,
                 top_ads: list,
                 bottom_ads: list,
                 related_queries: list,
                 questions: list,
                 top_stories: list,
                 news_results: list,
                 knowledge_graph: dict,
                 related_searches: list,
                 ):
        self.organic_results = [
            OrganicResult(**i) for i in organic_results
        ]
        self.searching_query = searching_query
        self.meta_data = meta_data
        self.local_results = local_results
        self.top_ads = top_ads
        self.bottom_ads = bottom_ads
        self.related_queries = related_queries
        self.questions = questions
        self.top_stories = top_stories
        self.news_results = news_results
        self.knowledge_graph = knowledge_graph
        self.related_searches = related_searches


def send_request(searching_query: SearchingQuery) -> ScrapingObject:
    response = requests.get(
        url="https://app.scrapingbee.com/api/v1/store/google",
        params=searching_query.to_dict(),

    )
    error_message = response.json().get('message')
    if not error_message:
        return ScrapingObject(searching_query=searching_query, **response.json())
    else:
        if 'Invalid api key' in error_message:
            raise ApiKeyError(response.json())
