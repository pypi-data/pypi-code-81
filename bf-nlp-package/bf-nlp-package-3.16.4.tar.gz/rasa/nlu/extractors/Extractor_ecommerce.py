from rasa.nlu.components import Component
from rasa.nlu import utils
from rasa.nlu.model import Metadata
import os
import pandas as pd
import typing
from typing import Any, Optional, Text, Dict
import numpy as np
import regex as re
from time import strftime
from datetime import datetime as dt
from typing import Any, Optional, Text, Dict
import numpy as np
import dateutil.parser as dparser
import datefinder

from dateutil.parser import parse
import datetime
import dateutil.parser as dparser
from pyarabic.number import text2number
import datefinder
from dateutil.parser import parse
from datetime import timedelta
from dateutil.relativedelta import relativedelta


from rasa.nlu.training_data import Message, TrainingData


class Extracteur_ecommerce(Component):
	"""A custom Ecom analysis component"""
	name = "Ecommerce_EXTRACTION"
	provides = ["entities"]
	requires = ["tokens"]
	defaults = {}
	language_list = ["en","fr"]
	print('initialised the class')

	def _init_(self, component_config=None):
		super(Extracteur_oncf, self)._init_(component_config)

	def train(self, training_data, cfg, **kwargs):
		"""Load the sentiment polarity labels from the text
		   file, retrieve training tokens and after formatting
		   data train the classifier."""

	
	def convert_to_size(self, value):
		"""Convert model output into the Rasa NLU compatible output format.""" 

		entity = {"value": value,
				  
				  "entity": "ENTITY_size",
				  "extractor": "extractor"}

		return entity
	def convert_to_type(self, value):
		"""Convert model output into the Rasa NLU compatible output format.""" 

		entity = {"value": value,
				  
				  "entity": "ENTITY_type",
				  "extractor": "extractor"}

		return entity
	def convert_to_color(self, value):
		"""Convert model output into the Rasa NLU compatible output format.""" 

		entity = {"value": value,
				  
				  "entity": "ENTITY_color",
				  "extractor": "extractor"}

		return entity	


	def process(self, message:Message , **kwargs):
		"""Retrieve the tokens of the new message, pass it to the classifier
			and append prediction results to the message class."""
		print(message.text)	
		if not self :
			entities = []
		else:

			tokens = [t.text for t in message.get("tokens")]
			print('***********tokens*****')
			print(tokens)
            
			entities_type = []
			entities_Size = []
			entities_Color = []
            
			Types_keys_fr = ["haut","robe","veste","pantalon","jupe","chaussure","pyjama","sac","accessoire","lunette"]
			
			
			list2 = []
			Types_values_fr = [["pull", "tshirt", "blouse", "chemise", "haut","tricot","top"],["robe"],["veste","manteau","doudoune"],["jean","pantalon","short","legging","jogging"],["jupe"],["bottes","chaussure","basket","espas","talons","sandale"],["pyjama"],["sac","cartable","pochette","sacoche"],["accessoire","bijoux","bague","collier","gourmette","boucle.oreille"],["lunette"]]
			Types_values_ar = [["تشيرت", "بلوزة"],["كسوة"],["معطف"],["سروال"],["تنورة"],["سباط"],["بيجاما"],["ساك"],["اكسسوار"],["ندادر"]]
			
			Types_values_ang = [["shirt"],["dress"],["coat"],["jeans"],["skirt"],["shoes"],["pyjama"],["purse"],["accessory"],["glasses"]]
			list1 = Types_values_fr
			
			for i in range(len(Types_values_fr)):
				print(Types_values_ar[2][0])
				for j in range(len(Types_values_ar[i])):
					list1[i].append(Types_values_ar[i][j])
				for j in range(len(Types_values_ang[i])):
					list1[i].append(Types_values_ang[i][j])
				
			print("list1")
			print(list1)
				
			Type_dictionary = dict(zip(Types_keys_fr, list1))
			#print(Type_dictionary)

			for w in tokens :
				for key in Type_dictionary :
					if w in Type_dictionary[key] :
						entities_type.append(key)
			
			entity_type = self.convert_to_type(entities_type)
			message.set("entities_type", entity_type, add_to_output=True)
			print("entities_type_Ecomm")
			



			
			Color_keys = ["noir","blanc","rouge","jaune","bleu","vert","orange","rose","marron","gris","mauve","beige"]

			Color_values_ar = [["noir"],["blanc"],["rouge"],["jaune"],["bleu"],["vert"],["orange"],["rose"],["marron"],["gris"],["mauve"],["beige"]]
			Color_values_fr = [["نوار"],["ابيض"],["روج"],["سفر"],["زرق"],["خدر"],["ليموني"],["روز"],["مارون"],["رمادي"],["موف"],["بيج"]]
			Color_values_ang = [["black"],["white"],["red"],["yellow"],["blue"],["green"],["orange"],["pink"],["brown"],["grey"],["mauve"],["beige"]]
			list2 = Color_values_fr
			
			for i in range(len(Types_values_fr)):
				print(Color_values_ar[2][0])
				for j in range(len(Color_values_ar[i])):
					list2[i].append(Color_values_ar[i][j])
				for j in range(len(Color_values_ang[i])):
					list2[i].append(Color_values_ang[i][j])
			Color_dictionary = dict(zip(Color_keys, list2))
			
			for w in tokens :
				for key in Color_dictionary :
					if w in Color_dictionary[key] :
						entities_Color.append(key)
			
			entity_color = self.convert_to_type(entities_Color)
			message.set("entities_color", entity_color, add_to_output=True)
			print("entities_colors_Ecomm")
			print(entity_color)
			print(Color_dictionary)
			print(Type_dictionary)

			

			Size_keys = ["M","S","L"]

			Size_values_fr = [["moyen", "moyenne", "m","medium"],["s","small","petit"],["l","large"]]
			Size_values_ar = [["مويان"],["صغير"],["لارج"]]
			Size_values_ang = [["medium"],["little"],["large,big"]]

			
			list3 = Size_values_fr
			for i in range(len(Size_values_fr)):
				
				for j in range(len(Size_values_ar[i])):
					list3[i].append(Size_values_ar[i][j])
				for j in range(len(Size_values_ang[i])):
					list3[i].append(Size_values_ang[i][j])
			Size_dictionary = dict(zip(Size_keys, list3))

			for w in tokens :
				for key in Size_dictionary :
					if w in Size_dictionary[key] :
						entities_Size.append(key)

			print(Size_dictionary)
			entity_size = self.convert_to_type(entities_Size)
			message.set("entities_size", entity_size, add_to_output=True)
			print("entities_size_Ecomm")
			print(entity_size)
