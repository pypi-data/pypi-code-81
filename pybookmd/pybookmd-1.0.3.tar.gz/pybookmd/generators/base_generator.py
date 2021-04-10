import os
from abc import ABC, abstractmethod

import pypandoc

from hash import has_hash_changed, write_new_hash


class BookGenerator(ABC):
	def __init__(self, build_args: dict): 
		self._unpack_build_args(build_args)
		self._perform_directory_checks()

	def _unpack_build_args(self, build_args):
		self.title = " ".join(build_args.title)
		self._output_file_name = "_".join(self.title)
		self.chapters_dir = build_args.chapters_dir
		self.output_dir = build_args.release_dir

	@property
	@abstractmethod
	def FILE_FORMAT(self) -> str:
		"""Output file format of the subclass
		"""
		pass

	def _perform_directory_checks(self):
		if not os.path.isdir(self.chapters_dir):
			raise IOError("Chapters Directory does not exist")
		if not os.path.isdir(self.output_dir):
			os.mkdir(self.output_dir)
		if not os.path.isdir(".hashes"):
			os.mkdir(".hashes")

	def generate_book(self):
		for (file_data, file_name) in self._read_chapters():
			data = self._format_data_pre_conversion(file_data) or file_data

			print(f"Checking contents for chapter file {file_name}")

			output_file_name = self._get_output_file_name(file_name)
			if has_hash_changed(data, file_name) is True or not os.path.exists(output_file_name):
				print(f"Content has changed for {file_name}, regenerating chapter")
				self._generate_chapter(file_name, data)
				write_new_hash(data, file_name)
			else:
				print(f"Content of {file_name} has not changed, skipping")

	def _read_chapters(self):
		for file_name in os.listdir(self.chapters_dir):
			file_path = f"{self.chapters_dir}/{file_name}"
			with open(file_path, "r") as fr:
				yield (fr.read(), file_name)

	@abstractmethod
	def _format_data_pre_conversion(self, file_data): 
		"""Hook method to tranform data before being pushed to pypandoc
		"""
		pass

	def _get_file_path(self, file_name):
		return f"{self.chapters_dir}/{file_name}"

	def _get_output_file_name(self, file_name):
		base_file_name = file_name.split(".")[0]
		return f"{self.output_dir}/{base_file_name}.pdf"

	def _generate_chapter(self, file_name, file_data):
		file_path = self._get_file_path(file_name)
		output_file_name = self._get_output_file_name(file_name)
		print(f"Generating file {output_file_name} with format {self.FILE_FORMAT}")
		try:
			output = pypandoc.convert_file(file_path, self.FILE_FORMAT, outputfile=output_file_name)
		except RuntimeError as e:
			err = str(e)
			print(f"Encountered error when generating new file, error: {err}")
