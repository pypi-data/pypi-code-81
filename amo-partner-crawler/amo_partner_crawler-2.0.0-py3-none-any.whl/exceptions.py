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


class AmoStartAccountException(BaseCrawlerException):
    message = 'Amo start account error'

    def __init__(self):
        super().__init__(message=self.message)


class BaseTariffAccountException(BaseCrawlerException):
    message = 'Base tariff account error'

    def __init__(self):
        super().__init__(message=self.message)


class TechAccountException(BaseCrawlerException):
    message = 'Tech account error'

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
