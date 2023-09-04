import webbrowser

from app import scrapingbee, database

searching_statement = ('inurl:'
                       'recommendation'
                       ' intext:'
                       '"friend\'s email"'
                       '')


def parse_donors():
    searching_query = scrapingbee.SearchingQuery(
        **dict(
            search=searching_statement,
            page=1,
            nb_results=100,
            # country_code='uk'
        )
    )
    scraping_object: scrapingbee.ScrapingObject = scrapingbee.send_request(searching_query)
    for res in scraping_object.organic_results:
        res.searching_query = searching_query
        database.OrganicResultsRepo.save_one(res)


def main():
    stmnt = {'searching_query.search': {'$regex': searching_statement}, 'status': 'not viewed'}
    results = database.OrganicResultsRepo.collection.find(stmnt, {})
    c = 0
    for result in results:
        print(result['url'])
        webbrowser.open(result['url'])
        result['status'] = 'viewed'
        database.OrganicResultsRepo.collection.update_one({'_id': result['_id']}, {'$set': result})
        c += 1
        if c > 10:
            input('enter:\n')
            c = 0


if __name__ == '__main__':
    parse_donors()
    main()
