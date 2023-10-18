from app import scrapingbee, config


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


def test_inner_send_request():
    params = {
        "api_key": config.SCRAPINGBEE_APIKEY,
        "search": "pizza new-york",
    }
    response = scrapingbee.__send_request(params)
    print(response.text)
    print(response)
    assert response.status_code < 400
