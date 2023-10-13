from app import scrapingbee, database, config

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

# inurl_list = '''
# inurl:contact-us
# inurl:contactus
# inurl:kontakt/
# inurl:contact.aspx
# inurl:ContactForm
# inurl:contact.php
# inurl:index.php
# inurl:contact
# inurl:contact.html
# '''.strip().split()

intext_list = '''
intext:"friend's email"
'''.strip().split()


def parse_donors(query: dict):
    searching_query = scrapingbee.SearchingQuery(**query)
    scraping_object: scrapingbee.ScrapingObject = scrapingbee.send_request(searching_query)
    organic_results: list[scrapingbee.OrganicResult] = scraping_object.organic_results
    for organic_result in organic_results:
        organic_result.searching_query = searching_query
        config.logger.info(f'saving {organic_result=}')
        database.OrganicResultsRepo.save_one(organic_result)


def inf_donors_parsing():
    c = 0
    while True:
        for intext_part in intext_list:
            for inurl_part in inurl_list:
                search = f'{inurl_part} {intext_part}'
                query = dict(
                    search=search,
                    page=c,
                    nb_results=100,
                    # country_code='uk'
                )
                config.logger.info(f'{query}')
                parse_donors(query)
        # if c >= 3:
        #     c = 0
        # else:
        #     c += 1


if __name__ == '__main__':
    inf_donors_parsing()
