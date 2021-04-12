import logging

from kouyierr import index
from kouyierr.commands import documentation
from kouyierr.commands import invoice
from kouyierr.commands import ghproject


def main() -> None:
    logging.basicConfig(format='%(message)s')
    logging.getLogger(__package__).setLevel(logging.INFO)
    invoice.register()
    documentation.register()
    ghproject.register()
    index.register()
    index.index()
