from app import scrapingbee

# -----------------------------
# todo
#   country code management
#   page management
#   spilt searching_statement into small pieces

# -----------------------------
# todo
#   save scraped data

# -----------------------------
# todo
#   mark viewed scraping result


def main():
    searching_statement = "intitle:contact intext:\"Send Me a Copy\""
    searching_query = scrapingbee.SearchingQuery(searching_statement)  # can raise ApiKeyError if empty
    scraping_object: scrapingbee.ScrapingObject = scrapingbee.send_request(searching_query)  # can raise ApiKeyError

    if not scraping_object:
        return
    for result in scraping_object.organic_results:
        print(result.url)


if __name__ == '__main__':
    main()
