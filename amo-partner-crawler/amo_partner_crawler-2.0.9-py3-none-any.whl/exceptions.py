import logging


class BaseCrawlerException(Exception):
    def __init__(self, message: str):
        self.message = message
        logging.warning(message)

    def __str__(self):
        return self.message


class AmoCrawlerException(BaseCrawlerException):
    message = 'Amo Crawler error'

    def __init__(self):
        super().__init__(message=self.message)


class ElementHiddenException(BaseCrawlerException):
    message = 'Element is not available but hidden!'

    def __init__(self):
        super().__init__(message=self.message)


class AlreadyPaidException(BaseCrawlerException):
    message = 'Already Paid error!'

    def __init__(self):
        super().__init__(message=self.message)


class IDNotFoundException(BaseCrawlerException):
    message = 'Account with same ID not found'

    def __init__(self):
        super().__init__(message=self.message)


class BadTariffException(BaseCrawlerException):
    message = 'Base tariff account error'

    def __init__(self):
        super().__init__(message=self.message)


class NotAuthorizeException(BaseCrawlerException):
    message = 'Need authenticate!'

    def __init__(self):
        super().__init__(message=self.message)


class FatalityException(BaseCrawlerException):
    message = 'Fatality!'

    def __init__(self):
        super().__init__(message=self.message)
