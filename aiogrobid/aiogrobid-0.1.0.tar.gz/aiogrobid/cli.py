import fire
from aiogrobid import GrobidClient
from aiokit.utils import sync_fu


async def process(base_url, pdf_file):
    async with GrobidClient(base_url=base_url) as c:
        return await c.process_fulltext_document(pdf_file)


def main():
    fire.Fire(sync_fu(process))


if __name__ == '__main__':
    main()
