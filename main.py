import webbrowser

from app import scrapingbee, database


def parse_donors(searching_query: scrapingbee.SearchingQuery):
    scraping_object: scrapingbee.ScrapingObject = scrapingbee.send_request(searching_query)
    for res in scraping_object.organic_results:
        res.searching_query = searching_query
        database.OrganicResultsRepo.save_one(res)


def find_donors(stmnt: dict):
    results = database.OrganicResultsRepo.collection.find(stmnt, {})
    c = 0
    for result in results:
        url = result['url']
        webbrowser.open(url)

        result['status'] = 'viewed'
        database.OrganicResultsRepo.collection.update_one({'_id': result['_id']}, {'$set': result})
        c += 1
        if c > 10:
            input('enter:\n')
            c = 0


def main():
    searching_statement = 'inurl:EmailToFriend intext:"friend\'s email"'
    searching_query = scrapingbee.SearchingQuery(
        **dict(
            search=searching_statement,
            page=1,
            nb_results=100,
            # country_code='uk'
        )
    )
    stmnt = {'searching_query.search': {'$regex': searching_statement}, 'status': 'not viewed'}
    parse_donors(searching_query)
    find_donors(stmnt)


if __name__ == '__main__':
    main()
