from app import config


def test_config():
    assert config.MONGO_URL is not None
    assert config.SCRAPINGBEE_APIKEY is not None
