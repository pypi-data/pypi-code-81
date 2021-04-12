class ReturnDTO:

    def __init__(self, ret: int = 1, error_code: str = None, message: str = None, data: dict = None):
        self.ret = ret
        self.error_code = error_code
        self.message = message
        self.data = data

    def to_dict(self) -> dict:
        return self.__dict__

    @staticmethod
    def success(message: str = None, data: dict = None) -> dict:
        return ReturnDTO(ret=1, message=message, data=data).to_dict()

    @staticmethod
    def fail(message: str = None, error_code: str = None, data: dict = None):
        return ReturnDTO(ret=0, message=message, error_code=error_code, data=data).to_dict()


class PageDTO(ReturnDTO):
    @staticmethod
    def success(page: int, page_size: int, total: int, message: str = None, data: dict = None) -> dict:
        return ReturnDTO(ret=1, message=message,
                         data={"page": page, "page_size": page_size, "total": total, "data": data}).to_dict()

    @staticmethod
    def fail(page: int, page_size: int, total: int, message: str = None, error_code: str = None, data: dict = None):
        return ReturnDTO(ret=0, message=message, error_code=error_code,
                         data={"page": page, "page_size": page_size, "total": total, "data": data}).to_dict()
