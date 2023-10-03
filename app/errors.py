class ScrapingBeeApiKeyError(Exception):
    ...


class ScrapingBeeUnexpectedError(Exception):
    ...


class ScrapingBeeMonthlyCallsReachedError(Exception):
    ...


class CantDecodeResponse(Exception):
    ...
