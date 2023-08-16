from app import scrapingbee


def test_SearchingQuery():
    query = scrapingbee.SearchingQuery(search='test')
    print(query)
    assert query is not None


def test_ScrapingObject():
    searching_statement = "intitle:contact intext:\"Send Me a Copy\""
    searching_query = scrapingbee.SearchingQuery(search=searching_statement)

    scraping_object: scrapingbee.ScrapingObject = scrapingbee.send_request(searching_query)
    print(scraping_object)
    assert scraping_object is not None
