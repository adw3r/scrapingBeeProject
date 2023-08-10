from app.scrapingbee import SearchingQuery, OrganicResult, ScrapingObject


def test_SearchingQuery():
    query = SearchingQuery(search='test')
    print(query)
