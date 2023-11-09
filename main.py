import time
import webbrowser

from app import database, config

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

intext_list = '''
intext:"friend's email"
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


def extract_donors(query: str):
    stmnt = {'searching_query.search': {'$regex': query}, 'status': 'not viewed'}
    config.logger.info(f'{stmnt=}')
    results = database.OrganicResultsRepo.collection.find(stmnt, {})
    c = 0
    res = False
    for result in results:
        url = result['url']
        webbrowser.open(url)

        result['status'] = 'viewed'
        database.OrganicResultsRepo.collection.update_one({'_id': result['_id']}, {'$set': result})
        c += 1
        if c > 10:
            input('enter:')
            c = 0
            res = True
    if res:
        input('enter:')
        res = False


def inf_extract_donors():
    while True:
        for intext_part in intext_list:
            for inurl_part in inurl_list:
                search = f'{inurl_part} {intext_part}'
                extract_donors(search)
                time.sleep(.2)


if __name__ == '__main__':
    inf_extract_donors()
