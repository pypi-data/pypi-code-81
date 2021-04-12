#!/usr/bin/python
# -*- coding: UTF-8 -*-

import psycopg2
import threading
import logging
from copy import deepcopy

class PostgresqlDBService(object):
	_instance_lock = threading.Lock()
	connection_kwargs = {}
	connect = None
	logger = None

	hasLog = False
	primaryKey = 'id'

	def __init__(self, *args, **kwargs):
		self.logger = logging.getLogger('PostgresqlDBService')
		self.connection_kwargs = kwargs
		self.connection()
	
	def try_except(self):
		def wrapper(*args, **kwargs):
			try:
				self(*args, **kwargs)
			except Exception as e:
				print("get error: %s" % e)
		return wrapper

	
	def connection(self):
		kwargs = self.connection_kwargs
		if 'host' in kwargs and 'user' in kwargs and 'passwd' in kwargs :
			host = kwargs['host']
			port = int(kwargs['port']) if 'port' in kwargs else 3306
			user = kwargs['user']
			passwd = kwargs['passwd']
			charset = kwargs['charset'] if 'charset' in kwargs else 'utf8'
			db = kwargs['db'] if 'db' in kwargs else 'example'

			try:
				self.connect = psycopg2.connect(host=host, user=user, password=passwd, database=db, port=port)
			except Exception as e:
				print(e)


	@classmethod
	def instance(cls, *args, **kwargs):
		if not hasattr(PostgresqlDBService, "_instance"):
			with PostgresqlDBService._instance_lock:
				if not hasattr(PostgresqlDBService, "_instance"):
					PostgresqlDBService._instance = PostgresqlDBService(*args, **kwargs)
		return PostgresqlDBService._instance

	def setPrimaryKey(self,key):
		self.primaryKey = key
		return self

	def setShowLog(self,isShow):
		self.hasLog = isShow
		return self

	def test(self):
		return {'state':2008,'data':'this is a test'}

	def getOne(self, table,input_query={},input_field='*',input_orderby=[]):
		query = deepcopy(input_query)
		field = deepcopy(input_field)
		orderby = deepcopy(input_orderby)
		sql = self._parse_query(table=table, query=query, field=field, orderby=orderby, limit=1)
		result = self.query_one(sql)
		return result

	def prevOne(self, table, id, input_query={}):
		result = None
		query = deepcopy(input_query)
		query[self.primaryKey] = {'<':id}
		sql = self._parse_query(table=table, query=query,field='*',orderby=[],limit=1)
		result = self.query_one(sql)
		return result
		
	def nextOne(self, table, id, input_query={}):
		result = None
		query = deepcopy(input_query)
		query[self.primaryKey] = {'>':id}
		sql = self._parse_query(table=table, query=query,field='*',orderby=[],limit=1)
		result = self.query_one(sql)
		return result

	def getPage(self, table, input_query={},input_field='*', input_orderby=[], page=1, size=50,input_expect=["user"]):
		
		query = deepcopy(input_query)
		field = deepcopy(input_field)
		orderby = deepcopy(input_orderby)
		expect = deepcopy(input_expect)
		sql = self._parse_query(table=table, query=query,field=field,orderby=orderby, page=page, size=size)
		result = self.query(sql)
		total = self.getCount(table, query)
		last = int(total/size) if total%size==0 else int(total/size) + 1
		return {'data':result,'page':{"total":total,"size":size,"page":page,"last":last}}

	def getList(self, table, input_query={},input_field='*', input_orderby=[],limit=None,input_expect=["user"]):
		query = deepcopy(input_query)
		field = deepcopy(input_field)
		orderby = deepcopy(input_orderby)
		expect = deepcopy(input_expect)
		sql = self._parse_query(table=table, query=query,field=field,orderby=orderby, limit=limit)
		result = self.query(sql)
		return result

	def save(self, table,input_data,input_key='id'):
		result = {}
		new_id = 0
		data = deepcopy(input_data)
		if input_key in data:
			new_id = data[input_key]
			oldData = self.getOne(table, {input_key:new_id},'*',[(input_key,1)])
			if oldData:
				update_data = {}
				for key in data:
					if key not in [input_key]:
						if (key in oldData and data[key] != oldData[key]) or (key not in oldData):
							if type(data[key]).__name__=='bytes':
								update_data[key] = data[key].decode('utf-8')
							else:
								update_data[key] = data[key]
				if update_data:
					self.modify(table, {input_key:new_id}, update_data)
			else:
				new_id = self.add(table, data)
		else:
			new_id = self.add(table, data)

		if new_id:
			result = self.getOne(table, {input_key:new_id},'*',[(input_key,1)])
		return result

	def add(self, table, input_data):
		result = None
		data = deepcopy(input_data)
		if data:
			sql = self._parse_insert_one(table, data)
			result = self.execute(sql)
		return result

	def modify(self, table,input_query,input_data):
		result = {}
		if input_data:
			query = deepcopy(input_query)
			data = deepcopy(input_data)
			sql = self._parse_update(table, query,data)
			result = self.execute(sql)
		return result
	
	def delete(self, table,input_query):
		query = deepcopy(input_query)
		sql = self._parse_del(table, query)
		result = self.execute(sql)
		return result

	def getCount(self, table, input_query={}):
		result = 0
		query = deepcopy(input_query)
		sql = 'select count(1) as count from '+ table + ' '
		where_sql = self._where(query)
		if where_sql:
			sql += 'where '+ where_sql 
		res = self.query_one(sql)
		if res:
			result = int(res['count'])
		return result

	def _parse_query(self, table, *args, **kwargs):
		query = kwargs['query'] if 'query' in kwargs else {}
		field = kwargs['field'] if 'field' in kwargs else '*'
		orderby = kwargs['orderby'] if 'orderby' in kwargs else []
		limit = kwargs['limit'] if 'limit' in kwargs else None
		page = int(kwargs['page']) if 'page' in kwargs else 0
		size = int(kwargs['size']) if 'size' in kwargs else 0

		if page and size:
			begin = (page -1 )* size
			limit = str(size)+' offset '+str(begin)

		field_where = self._field(field)

		sql = 'select ' + field_where + ' from "'+ table + '" '
		where_sql = self._where(query)
		if where_sql:
			sql += 'where '+ where_sql + ' '
		order_sql = self._order(orderby)
		if order_sql:
			sql += order_sql + ' '
		limit_sql = self._limit(limit)
		if limit_sql:
			sql +=  limit_sql + ' '
		return sql
	
	def _parse_insert_one(self, table, data):
		sql = 'insert into "'+ table + '" '
		columns = []
		for key in data:
			if key not in columns:
				columns.append(key)
		sql += ' ("' + '", "'.join(columns) + '") values (\''
		tmp = []
		for key in columns:
			if key in data:
				if type(data[key]).__name__=='bool':
					sql = sql[:-1]+str(data[key])+",'"
				else:
					sql += str(data[key])+"','"
			else:
				sql += ""
		sql = sql[:-2] + ") returning *;"

		return sql

	def _parse_update(self, table, query, data):
		sql = ''
		data_sql = ''
		for key in data:
			if type(data[key]).__name__=='bool':
				data_sql += '"'+key + "\"="+str(data[key])+", "
			else:
				data_sql += '"'+key + "\"='"+str(data[key])+"', "
		if data_sql:
			sql = 'update "'+ table + '" set ' + data_sql[0:-2]
		where_sql = self._where(query)
		if where_sql:
			sql = sql + ' where '+ where_sql + ' '
		return sql

	def _parse_del(self, table, query):
		where_sql = self._where(query)
		if where_sql:
			where_sql = 'where '+ where_sql + ' '

		sql = 'delete from  '+ table + ' ' + where_sql
		return sql
		
	def _field(self,query):
		sql = ''
		if type(query).__name__=='tuple':
			query = list(query)
		if type(query).__name__=='list':
			sql = '"'+'","'.join(query)+'"'
		elif not query or query == '*':
			sql = '*'
		else:
			sql = '"'+query+'"'
		return sql

	def _where(self,query):
		sql = ''
		if type(query).__name__=='dict':
			for key in query:
				opeartor = '='
				value = ''
				if type(query[key]).__name__!='dict':
					tmp = {'=':query[key]}
				else:
					tmp = query[key]
				for k in tmp:
					opeartor = k
					if type(tmp[k]).__name__=='bool':
						sql += '"'+key + '" ' + opeartor + ""+ str(tmp[k]) + " and "
					else:
						sql += '"'+key + '" ' + opeartor + "'"+ str(tmp[k]) + "' and "
				
		return sql[0:-4]

	def _order(self,orderby):
		if len(orderby) > 0:
			sql = 'order by '
			for item in orderby:
				order = item[0]
				sort = 'asc' if item[1]==1 else 'desc'
				sql += '"'+order+'" ' + sort + ','
			return sql[0:-1]
		return ''

	def _limit(self,limit):
		if limit:
			if type(limit).__name__ == 'string':
				return 'limit '+ limit
			elif type(limit).__name__ == 'int':
				return 'limit '+ str(limit)
			else:
				temp = list(limit)
				if len(temp) == 2:
					return 'limit ' + temp[0] + ' offset '+ temp[1]
			return 'limit ' + limit
		else:
			return ''
	
	def query_one(self, sql, params=None):
		cur = None
		result = None
		column_names = []
		data_rows = []
		if self.connect:
			try:
				cur = self.connect.cursor()
				if self.hasLog:
					self.logger.info(sql)
				count = cur.execute(sql,params)
				column_names = [desc[0] for desc in cur.description]
				for row in cur:
					data_rows =dict(zip(list(column_names),row))
				self.connect.commit()
			except Exception as e:
				self.connect.rollback()
				print(" Error:%s" % e)
			finally:
				if cur:
					cur.close()
		return data_rows

	def queryAndFlag(self, table,input_query={},input_flag={}):
		cur = None
		result = None
		query = deepcopy(input_query)
		sql1 = self._parse_query(table=table, query=query,limit=1)
		if self.connect:
			try:
				cur = self.connect.cursor()
				if self.hasLog:
					self.logger.info(sql1)
					print(sql1)
				count = cur.execute(sql1)
				info = cur.fetchone()
				if info:
					data = deepcopy(input_flag)
					sql2 = self._parse_update(table,{self.primaryKey:info[self.primaryKey]},data)
					if self.hasLog:
						self.logger.info(sql2)
						print(sql2)
					count = cur.execute(sql2)
					sql3 = self._parse_query(table,query={self.primaryKey:info[self.primaryKey]},limit=1)
					count = cur.execute(sql3)
					if self.hasLog:
						self.logger.info(sql3)
						print(sql3)
					result = cur.fetchone()
				self.connect.commit()
			except Exception as e:
				self.connect.rollback()
				print("Error:%s" % e)
			finally:
				if cur:
					cur.close()
		return result

	def query(self, sql, params=None):
		cur = None
		result = None
		column_names = []
		data_rows = []
		if self.connect:
			try:
				cur = self.connect.cursor()
				if self.hasLog:
					self.logger.info(sql)
					print(sql)
				count = cur.execute(sql,params)
				column_names = [desc[0] for desc in cur.description]
				for row in cur:
					data_rows.append(dict(zip(list(column_names),row)))
				self.connect.commit()
			except Exception as e:
				self.connect.rollback()
				print(" Error:%s" % e)
			finally:
				if cur:
					cur.close()
		return data_rows

	def execute(self, sql, params=None):
		cur = None
		count = 0
		if self.connect:
			try:
				cur = self.connect.cursor()
				if self.hasLog:
					self.logger.info(sql)
					print(sql)
				count = cur.execute(sql,params)
				self.connect.commit()
			except Exception as e:
				if self.connect:
					self.connect.rollback()
				print("Error:%s" % e)
			finally:
				if cur:
					cur.close()
		return count

	def close(self):
		if self.connect:
			self.connect.close()

	def __del__(self):
		self.close()
	
if __name__ == "__main__":
	db = PostgresqlDBService.instance(host='localhost', port=3306, user='root', passwd='123456', db='example', charset='utf8')
	result = db.query('select * from data',())
	print(result)