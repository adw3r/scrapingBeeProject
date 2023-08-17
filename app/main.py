from app import scrapingbee, database

import webbrowser


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


def main():
    results = database.OrganicResultsRepo.collection.find({'status': 'not viewed'}, {})
    c = 0
    for result in results:
        webbrowser.open(result['url'])

        print(result)
        result['status'] = 'viewed'
        res = database.OrganicResultsRepo.collection.update_one(
            {'_id': result['_id']}, {'$set': result}
        )
        c += 1
        if c > 10:
            input('enter:\n')
            c = 0


if __name__ == '__main__':
    main()
