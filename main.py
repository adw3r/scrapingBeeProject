import webbrowser

from app import scrapingbee, database, config


def parse_donors(query: dict):
    searching_query = scrapingbee.SearchingQuery(**query)
    scraping_object: scrapingbee.ScrapingObject = scrapingbee.send_request(searching_query)
    organic_results: list[scrapingbee.OrganicResult] = scraping_object.organic_results
    for organic_result in organic_results:
        organic_result.searching_query = searching_query
        config.logger.info(f'saving {organic_result=}')
        database.OrganicResultsRepo.save_one(organic_result)


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
            input('enter:')
            c = 0


def main():
    inurl_list = '''
    inurl:email-to-friend
    inurl:EmailToFriend
    inurl:emailfriend.asp
    inurl:email-recipe
    inurl:forward-to-a-friend
    inurl:invite-friend-subscribe.php
    inurl:refer-a-friend
    inurl:refer
    inurl:tellafriend.asp
    inurl:TellAFriend
    inurl:tell.php
    inurl:tell
    inurl:tellafriend.php
    inurl:tell-friend
    inurl:tell-a-friend
    inurl:recommend
    inurl:recommend-a-friend
    inurl:recommend-us
    inurl:recommendation
    inurl:share.html
    inurl:share
    inurl:refer-friend.php
    inurl:Default.aspx
    inurl:contact-us
    inurl:contact
    inurl:Contact.php
    inurl:form
    inurl:feedback
    inurl:suggest-a-friend.php
    inurl:suggest.php
    inurl:mailto
    inurl:send-to-friend
    inurl:send
    inurl:suggest
    inurl:forward
    inurl:referral-rewards
    '''.strip().split()
    for part in inurl_list:
        query = dict(
            search=f'{part} intext:"friend\'s email"',
            page=2,
            nb_results=100,
            # country_code='uk'
        )
        stmnt = {'searching_query.search': {'$regex': query['search']}, 'status': 'not viewed'}
        config.logger.info(f'{stmnt=}')
        parse_donors(query)
        find_donors(stmnt)
        input('enter:')


if __name__ == '__main__':
    main()
