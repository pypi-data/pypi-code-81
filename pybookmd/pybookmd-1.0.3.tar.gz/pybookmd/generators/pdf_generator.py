from .base_generator import BookGenerator

class PDFGenerator(BookGenerator):

	FILE_FORMAT = "pdf"

	def _format_data_pre_conversion(self, file_data): 
		pass
