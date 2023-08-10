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
    searching_query = scrapingbee.SearchingQuery(search=searching_statement)
    scraping_object: scrapingbee.ScrapingObject = scrapingbee.send_request(searching_query)

    for result in scraping_object.organic_results:
        print(result)


if __name__ == '__main__':
    main()
