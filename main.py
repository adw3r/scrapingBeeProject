import scrapingbee


def main():
    # -----------------------------
    # todo
    #   country code management
    #   page management
    #   spilt searching_statement into small pieces

    searching_statement = "intitle:contact intext:\"Send Me a Copy\""
    scraping_params = {
        "search": searching_statement,
        "country_code": "gb",
        "page": 2
    }

    # -----------------------------
    # todo
    #   save scraped data

    scraping_object: scrapingbee.ScrapingObject = scrapingbee.send_request(scraping_params)  # can raise ApiKeyError
    if not scraping_object:
        return

    # -----------------------------
    # todo
    #   mark viewed scraping result

    for item in scraping_object.organic_results:
        print(item)


if __name__ == '__main__':
    main()
