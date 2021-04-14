# -*- coding: utf-8 -*-
# @Author: ander
# @Date:   2021-04-14 16:14:21
# @Last Modified by:   ander
# @Last Modified time: 2021-04-14 17:23:26
import comtypes.client
import os


class PPTXConvertor:

	# https://docs.microsoft.com/en-us/office/vba/api/powerpoint.ppsaveasfiletype
	filetype_map = {
		'AddIn': 8,
		'AnimatedGIF': 40,
		'BMP': 19,
		'Default': 11,
		'EMF': 23,
		'ExternalConverter': 64000,
		'GIF': 16,
		'JPG': 17,
		'MetaFile': 15,
		'MP4': 39,
		'OpenDocumentPresentation': 35,
		'OpenXMLAddin': 30,
		'OpenXMLPicturePresentation': 36,
		'OpenXMLPresentation': 24,
		'OpenXMLPresentationMacroEnabled': 25,
		'OpenXMLShow': 28,
		'OpenXMLShowMacroEnabled': 29,
		'OpenXMLTemplate': 26,
		'OpenXMLTemplateMacroEnabled': 27,
		'OpenXMLTheme': 31,
		'PDF': 32,
		'PNG': 18,
		'Presentation': 1,
		'RTF': 6,
		'Show': 7,
		'StrictOpenXMLPresentation': 38,
		'Template': 5,
		'TIF': 21,
		'WMV': 37,
		'XMLPresentation': 34,
		'XPS': 33,
	}

	def __init__(self, input_folder, output_folder):
		self.input_folder = input_folder
		self.output_folder = output_folder
		if not os.path.exists(self.output_folder):
			os.mkdir(self.output_folder)

	def convert(self, output_type='PDF'):
		if output_type in self.filetype_map:
			output_type_num = self.filetype_map[output_type]
		else:
			raise ValueError("Wrong output type. Must be one of [AddIn, AnimatedGIF, BMP, Default, EMF, ExternalConverter, GIF, JPG, MetaFile, MP4, OpenDocumentPresentation, OpenXMLAddin, OpenXMLPicturePresentation, OpenXMLPresentation, OpenXMLPresentationMacroEnabled, OpenXMLShow, OpenXMLShowMacroEnabled, OpenXMLTemplate, OpenXMLTemplateMacroEnabled, OpenXMLTheme, PDF, PNG, Presentation, RTF, Show, StrictOpenXMLPresentation, Template, TIF, WMV, XMLPresentation, XPS]")
		self.powerpoint = comtypes.client.CreateObject("Powerpoint.Application")
		self.powerpoint.Visible = 1
		for file in os.scandir(self.input_folder):
			if file.is_file() and file.name.endswith((".ppt", ".pptx")):
				output_path = os.path.join(self.output_folder, os.path.splitext(file.name)[0]) + '.pdf'
				deck = self.powerpoint.Presentations.Open(file.path)
				deck.SaveAs(output_path, output_type_num)
				deck.Close()
		self.powerpoint.Quit()
