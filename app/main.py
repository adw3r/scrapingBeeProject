from app import scrapingbee, database


def parse_donors():
    searching_statement = "inurl:contactus intext:\"Send Me a Copy\""
    d = dict(
        search=searching_statement,
        page=1,
        nb_results=100,
        # country_code='uk'
    )
    searching_query = scrapingbee.SearchingQuery(**d)
    scraping_object: scrapingbee.ScrapingObject = scrapingbee.send_request(searching_query)
    print(f'{scraping_object!r}')
    for res in scraping_object.organic_results:
        database.OrganicResultsRepo.save_one(res)


if __name__ == '__main__':
    parse_donors()
