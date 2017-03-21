"""
This class provide the database DML operations

@author Ideas2it
"""

import sqlite3
from DBConnector import DBConnector

class DBManipulation(object):

	def __init__(self, connection):
		self._connection = connection

	@property
	def connection(self):
		return self._connection
		
	def create_table(self, table_string):
		""" Function used to create the table at runtime

		@params table string - which have the table creation query
		"""
		if table_string:
			conn = self.connection
			cursor = conn.cursor()
			cursor.execute(table_string)
			print('Table created successfully ...')
		else:
			print('Table creation failed ...')
			raise Exception('Table creation string is empty')


	def many_insert_query_executor(self, query, query_data):
		""" Sqlite query executor which support multiple data insert at a time

		@params query - which have the insertion query with parameters
		@params query_data - which contains the dictionary of tuples
		@return bool
		"""
		if query:
			if query_data == None:
				raise Exception('Mass insertion data was empty ...')
			conn = self.connection
			cursor = conn.cursor()
			cursor.executemany(query, query_data)
			conn.commit()
			return True
		else:
			raise Exception('Query string is empty')	

	def insert_query_executor(self, query):
		""" Sqlite query executor which support only one query to execute at a time

		@params query - which have the insertion query with parameters
		@params query_data - which contains the dictionary of tuples
		@return bool
		"""
		if query:
			conn = self.connection
			cursor = conn.cursor()
			cursor.execute(query)
			conn.commit()
			return True
		else:
			raise Exception('Query string is empty')

if __name__ == "__main__" :
	conn = DBManipulation('')

