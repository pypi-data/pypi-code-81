from .base_generator import BookGenerator
from .pdf_generator import PDFGenerator


GENERATOR_BY_OUTPUT_FORMAT = {cls.FILE_FORMAT: cls for cls in BookGenerator.__subclasses__()}
