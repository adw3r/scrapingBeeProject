from app import database


def test_database():
    assert database.mongo_client.server_info() is not None
