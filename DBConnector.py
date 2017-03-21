"""
This act as bridge to connection to make unstructured data to structure data
and keep in sqlite database

@author Ideas2it
"""

import sqlite3

class DBConnector(object):

	def __init__(self, connection, schemaName):
		self._connection = connection
		self._schemaName = schemaName

	@property
	def connection(self):
		return self._connection

	@property
	def schemaName(self):
		return self._schemaName

	def create_schema(self):
		""" 
		Function used to create the database schema to store tables

		@params schemaName
		@returns database connection					
		"""
		try:
			self._connection = sqlite3.connect(self.schemaName)
			return self._connection;
		except Exception as ex:
			print('Exception while creating DB connection ', ex)

	def getConnection(self):
		if self._connection != null :
			return self._connection
		else :
			self.create();

	def closeConnection(self):
		self._connection.close();

if __name__ == "__main__" :
	print('Function calling main')
	conn = DBConnector('',"SoftCmpyInfo.db")
	conn.create()

