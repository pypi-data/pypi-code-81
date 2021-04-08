import pytest
from delphai_company_pages.pages import get_pages
import os
from dotenv import load_dotenv

test_domains = ['3emotion.eu', 'acerta.ai', 'www.waihigold.co.nz']
load_dotenv()
connection_string = os.environ.get('BLOB_CONNECTION_STRING')
container = os.environ.get('BLOB_CONTAINER')


@pytest.mark.asyncio
@pytest.mark.parametrize('domain', test_domains)
async def test_add_article(domain: str):
  pages = await get_pages(connection_string, container, domain)
  assert len(pages.pages) > 0
  assert pages.graph is not None