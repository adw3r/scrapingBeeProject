import random
from app import database, scrapingbee


def test_database_is_connected():
    assert database.mongo_client.admin.command('ping') == {'ok': 1.0}


def test_database_organic_result_repo_save_one():
    searching_statement = "intitle:contact intext:\"Send Me a Copy\""
    searching_query = scrapingbee.SearchingQuery(search=searching_statement)
    scraping_object: scrapingbee.ScrapingObject = scrapingbee.send_request(searching_query)

    org_res_model: dict = random.choice(scraping_object.organic_results).model_dump()
    result = scrapingbee.OrganicResult(**org_res_model)
    database.OrganicResultsRepo.save_one(result)


def test_database_organic_result_repo_find():
    results: list[dict] = database.OrganicResultsRepo.find()
    print(results)

    for i in results:
        assert type(i) is dict


def test_database_organic_result_repo_save_many():
    searching_statement = "intitle:contact intext:\"Send Me a Copy\""
    searching_query = scrapingbee.SearchingQuery(search=searching_statement)
    scraping_object: scrapingbee.ScrapingObject = scrapingbee.send_request(searching_query)

    res = database.OrganicResultsRepo.save_many(scraping_object.organic_results)
    print(res)
