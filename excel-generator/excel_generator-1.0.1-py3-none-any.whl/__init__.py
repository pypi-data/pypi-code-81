"""Generate Excel from JSON input file
Import the `Generator` to generate the Excel:
    >>> from excel_generator.generator import Generator
    >>> json_file = "results.json"
    >>> excel_file = "Results.xls"
    >>> generator = Generator(json_file=json_file, excel_file=excel_file)
    >>> generator.generate()
See https://github.com/estuaryoss/test-libs-python/tree/master/excel_generator for more information
"""

__version__ = "1.0.0"
