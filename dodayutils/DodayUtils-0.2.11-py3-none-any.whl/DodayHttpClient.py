#-*-coding:utf-8 -*-
from DodayUtils._dwrappers import *
import requests
import urllib.parse
import datetime
# from Cryptodome.Hash import SHA256, HMAC
# from base64 import b64decode, b64encode

class DodayHttpClient:
	"""
	This is the http client
	class. 
	"""
	def __init__(self, **configs):
		for key in configs:
			if "_http_url" in key:
				setattr(self, key, configs[key])

	def __getitem__(self, key):
		return getattr(self, key)
	
	@dutils	
	def client_get(self, key, input_dict, **configs):
		
		# authentication
		# a = GadgethiAuthenticationStandardEncryption(configs['gadgethi_key'],configs['gadgethi_secret'])
		# headers = a.authentication_encryption()
		
		get_query = self[key]

		# assign query list
		query_list = ["?"]
		for key in input_dict:
			query_list.extend([str(key), "=", input_dict[key], "&"])

		# concatenate together
		get_query += "".join(query_list[:-1])

		r = requests.get(get_query)
		response = r.text 
		return response
		
	@dutils	
	def client_post(self, key, input_dict, urlencode=False, **configs):
		# authentication
		# a = GadgethiAuthenticationStandardEncryption(configs['gadgethi_key'],configs['gadgethi_secret'])
		# headers = a.authentication_encryption()
		post_query = self[key]

		if urlencode:
			r = requests.post(post_query, data=input_dict)
		else:
			r = requests.post(post_query, json=input_dict)
		response = r.text

		return response


# class GadgethiAuthenticationStandardEncryption():
# 	# First the header should increase two fields (1) key (2) secret (3) time
# 	# key and the secret will be given 
# 	# You need to put key, time, hmac_result in the header file 
# 	# Please call authentication to get the need information dictionary in the header file
# 	def __init__(self,key,secret):
# 		self.key = str(key) 
# 		self.secret = str(secret)
# 	def HMAC256_digest(self,secret,string,mode='base64'):
# 		# we give secret type is string
# 		if type(secret) != bytes:
# 			secret = secret.encode()
# 		h = HMAC.new(secret, digestmod=SHA256)
# 		if string != bytes:
# 			string = string.encode()
# 		h.update(string)
# 		if mode != 'base64':
# 			return h.hexdigest()
# 		else:
# 			b64 = b64encode(bytes.fromhex(h.hexdigest())).decode()
# 			return b64
# 	def HMAC256_encryption(time_shift):
# 		# We standardize Taipei as the standard time
# 		localtime = int(datetime.datetime.utcnow().timestamp()) + (time_shift*60*60)
# 		encryption_result = self.HMAC256_digest(self.secret,self.key+str(localtime))
# 		return encryption_result

# 	def time_standard(time_shift):
# 		return int(datetime.datetime.utcnow().timestamp()) + (time_shift*60*60)

# 	def authentication_encryption(time_shift=8):
# 		authentication_dictionary = {}
# 		authentication_dictionary['gadgethi_key'] = self.key
# 		authentication_dictionary['HMAC256_result'] = HMAC256_encryption(time_shift)
# 		authentication_dictionary['time'] = time_standard(time_shift)
# 		return authentication_dictionary
