from elasticsearch import Elasticsearch
import datetime
import hashlib

class logMe():

	def __init__(self, hostname, port, log_index='logs_goes'):

		self.log_index = log_index
		self.es = Elasticsearch([{'host': hostname, 'port': port, 'url_prefix': 'es'}])
		self._id = hashlib.sha256(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")).encode('utf-8')).hexdigest()
			
	def create_doc(self, **kwargs):
			
		# get kwargs to log
		tuple_of_kwargs = (('date', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
											('search_agent', kwargs.get('search_agent')),
											('query_parameters', kwargs.get('query_parameters')),
											('query_id', kwargs.get('query_id')),
											('urls_google', kwargs.get('urls_google')),
											('retrieved_profiles_es', kwargs.get('retrieved_profiles_es')),
											('retrieved_profiles_query', kwargs.get('retrieved_profiles_query')),
											('running_pid', kwargs.get('running_pid')),
											('current_pid', kwargs.get('current_pid')),
											('execution_time', kwargs.get('execution_time')),
											('urls_google', kwargs.get('urls_google')),
											('SA_log', kwargs.get('SA_log')),
											('other', kwargs.get('other')))

		# create document to index
		doc_log = {k: v for k, v in tuple_of_kwargs if v is not None}
		
		return doc_log

	def log(self, **kwargs):
			
		doc_log = self.create_doc(**kwargs)

		# index document
		if not self.es.exists(index=self.log_index, id=self._id):
			self.es.index(index=self.log_index, id=self._id, body=doc_log)
		else:
			doc_log = {'doc': doc_log}
			self.es.update(index=self.log_index, id=self._id, body=doc_log)
