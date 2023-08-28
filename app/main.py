import webbrowser

from app import scrapingbee, database

searching_statement = "inurl:contact intext:\"Send copy to me\""


def parse_donors():
    d = dict(
        search=searching_statement,
        page=1,
        nb_results=100,
        # country_code='uk'
    )
    searching_query = scrapingbee.SearchingQuery(**d)
    scraping_object: scrapingbee.ScrapingObject = scrapingbee.send_request(searching_query)
    for res in scraping_object.organic_results:
        res.searching_query = searching_query
        database.OrganicResultsRepo.save_one(res)


def main():
    stmnt = {'searching_query.search': {'$regex': searching_statement}, 'status': 'not viewed'}
    results = database.OrganicResultsRepo.collection.find(stmnt, {})
    c = 0
    results_ = [i for i in results]
    print(len(results_))
    for result in results_:
        print(result['url'])
        webbrowser.open(result['url'])
        result['status'] = 'viewed'
        res = database.OrganicResultsRepo.collection.update_one({'_id': result['_id']}, {'$set': result})
        c += 1
        if c > 10:
            input('enter:\n')
            c = 0


if __name__ == '__main__':
    parse_donors()
    main()
