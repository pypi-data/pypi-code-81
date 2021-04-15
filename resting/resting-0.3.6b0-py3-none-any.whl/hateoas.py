

class HateoasParser:
    """
    Base Hateoas driver
    """
    def process(self, data=None, response=None):
        """
        Override this method when you write your own Hateoas driver

        :param requests.Response response: Response instance
        :param dict data: response data
        :return:
        """
        raise NotImplemented("Override this method in your class")


class SimpleLinksParser(HateoasParser):
    """
    SimpleLinksDriver parse links from response object like this

    {
        ...
        links: {
            "self": "http://localhost:8080/api/foo/1",
            ...
       }
    }


    """

    def process(self, data=None, response=None):
        if 'links' not in data:
            return
        return data.pop('links')


class SimpleUrlParser(HateoasParser):
    """
    To be deleted
    """
    def process(self, data=None, response=None):
        if 'url' in data:
            return {'self': data['url']}


# manager = HateoasManager(settings.HATEOAS_PARSERS)
