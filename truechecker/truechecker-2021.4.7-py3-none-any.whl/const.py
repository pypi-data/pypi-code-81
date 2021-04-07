from enum import Enum


class HTTPMethods(str, Enum):
    PUT = "PUT"
    GET = "GET"
    DELETE = "DELETE"
