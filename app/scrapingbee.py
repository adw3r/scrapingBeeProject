from datetime import datetime
from typing import Literal

import pydantic
import requests

from app import config, errors


class SearchingQuery(pydantic.BaseModel):
    search: str
    page: int = 1
    api_key: str = config.SCRAPINGBEE_APIKEY
    add_html: bool = False
    extra_params: str = ''
    country_code: str = 'us'
    language: str = 'en'
    nb_results: int = 100
    device: str = 'desktop'
    search_type: str = 'classic'


class OrganicResult(pydantic.BaseModel):
    url: str
    displayed_url: str
    position: int
    title: str
    domain: str
    sitelinks: list | dict
    rich_snippet: dict
    description: str | None = None
    date: str | None = None
    date_utc: str | None = None
    status: Literal['not viewed', 'viewed'] | str = 'not viewed'
    created_at: datetime = pydantic.Field(default_factory=datetime.now)
    searching_query: SearchingQuery | None = None


class ScrapingObject(pydantic.BaseModel):
    organic_results: list[OrganicResult] = []
    created_at: datetime = pydantic.Field(default_factory=datetime.now)
    meta_data: dict = {}
    local_results: list = []
    top_ads: list = []
    bottom_ads: list = []
    related_queries: list = []
    questions: list = []
    top_stories: list = []
    news_results: list = []
    related_searches: list = []
    knowledge_graph: dict = {}


def send_request(searching_query: SearchingQuery) -> ScrapingObject:
    params: dict = searching_query.model_dump()
    response = requests.get(
        url="https://app.scrapingbee.com/api/v1/store/google",
        params=params,
        verify=False
    )
    error_message = response.json().get('message')

    if error_message:
        __match_error(error_message)
    else:
        return ScrapingObject(**response.json())


class __MatchError:

    def __init__(self, error_message):
        self.error_message = error_message

    def __eq__(self, other) -> bool:
        return other in self.error_message


def __match_error(error_message):
    match __MatchError(error_message):
        case 'Invalid api key':
            raise errors.ScrapingBeeApiKeyError(error_message)
        case 'Monthly API calls limit reached':
            raise errors.ScrapingBeeMonthlyCallsReachedError(error_message)
        case _:
            raise errors.ScrapingBeeUnexpectedError(error_message)
