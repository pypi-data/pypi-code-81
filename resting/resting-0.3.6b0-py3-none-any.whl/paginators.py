import re

from .logger import logger


class Paginator:
    """
    Base Paginator class
    """

    def process(self, response, data):
        msg = "Override method process in your paginator to get it work"
        raise NotImplementedError(msg)


class HeaderPaginator(Paginator):
    """
    Parse pagination from response headers in format
    Content-Range:
        <str: name of entity> <int: start>/<int: end>/<int: total entities>
    Link: <http://localhost/books?limit=20&offset=40> rel="next",
        <http://localhost/books?limit=20&offset=0> rel="prev",
    """

    def process(self, response, data):

        headers = response.headers
        if 'Link' not in headers or 'Content-Range' not in headers:
            return {}

        parts = headers['Link'].split(',')

        pagination = {}
        for part in parts:
            url = re.match('<(.*)>', part)
            if not url:
                break
            url = url.group(1)

            result = re.match('.+rel=\"(prev|next)\"', part)
            if not result:
                break

            pagination[result.group(1)] = url

        result = re.match(r'^(.+) ([0-9]+)-([0-9]+)/([0-9]+)$',
                          headers['Content-Range'])
        if not result:
            msg = "Header 'Content-Range' is malformed. Got {}".format(
                headers['Content-Range'])
            logger.debug(msg)
        pagination['count'] = int(result.group(4))
        pagination['start'] = int(result.group(2))
        pagination['end'] = int(result.group(3))
        return pagination
