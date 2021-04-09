from aiobaseclient import BaseClient
from lxml import etree

from .exceptions import BadRequestError


class GrobidClient(BaseClient):
    def __init__(
        self,
        base_url: str,
        user_agent: str = None,
        max_retries=2,
        retry_delay=0.5,
    ):
        headers = {}
        if user_agent:
            headers['User-Agent'] = user_agent
        super().__init__(
            base_url=base_url,
            default_headers=headers,
            max_retries=max_retries,
            retry_delay=retry_delay,
        )

    def _find(self, root, name):
        r = root.find(name)
        if r is not None:
            return r.text

    async def process_fulltext_document(self, pdf_file):
        return await self.post(
            '/api/processFulltextDocument',
            data={
                'input': pdf_file,
            },
        )

    async def response_processor(self, response):
        content = await response.read()
        if response.status != 200:
            raise BadRequestError(status=response.status)
        try:
            root = etree.XML(content)
        except etree.XMLSyntaxError as e:
            raise BadRequestError(nested_error=e)
        return {
            'doi': self._find(root, ".//{http://www.tei-c.org/ns/1.0}idno[@type='DOI']"),
            'title': self._find(root, ".//{http://www.tei-c.org/ns/1.0}title[@level='a'][@type='main']"),
        }
