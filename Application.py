"""
This class act Interaction screen which get input from the user.
Here we declared our required information as global and static declaration

@author Ideas2it
"""

import sqlite3
from DBConnector import DBConnector
from DBManipulation import DBManipulation
from ConsoleAPIRequest import ConsoleAPIRequest
import sys
import time

class Application(object):

	# here we declared the static values which are refered with this class
	BASE_URL = 'https://maps.googleapis.com/maps/api'
	PLACE_URL = BASE_URL + '/place'
	TEXT_SEARCH_API_URL = PLACE_URL + '/textsearch/json?'
	NEARBY_SEARCH_API_URL = PLACE_URL + '/nearbysearch/json?'
	RESPONSE_STATUS_OK = 'OK'

	CREATE_TABLE_QUERY = "CREATE TABLE software_companies(   ID INTEGER PRIMARY KEY   AUTOINCREMENT,   address           TEXT,geometry TEXT, icon TEXT, google_id TEXT, name TEXT, place_id TEXT, rating TEXT, reference TEXT, types TEXT, photos TEXT, url TEXT)"

	GOOGLE_API_KEY = "AIzaSyAP10Oq3AJMhkFsWrN9OfR7HKPcr1li1_s"

	INSERT_QUERY = "INSERT INTO software_companies (address,geometry, icon,google_id,name,place_id,rating,reference,types,photos,url) VALUES(?,?,?,?,?,?,?,?,?,?,?)"

	def __init__(self, api_key):
		self._api_key = api_key
	
	@property
	def api_key(self):
        	return self._api_key

	def make_api_search(self, list_data, next_token):
		""" This function used to get API call and process the response"""
		
		try:
			api_request = ConsoleAPIRequest(self.api_key)
			geo_code = {'lat':'13.0145277', 'lng':'80.1981142'}
			query = 'software+company'
			response = api_request.company_search(self.TEXT_SEARCH_API_URL, query,geo_code,None,next_token)
			self.process_response(response)
			time.sleep(5)
			if response.has_next_page_token and response.raw_response['status'] == Application.RESPONSE_STATUS_OK :
				next_token = response.next_page_token
				self.make_api_search(list_data, next_token)
			return list_data
		except Exception as ex:
			raise Exception(str(ex))

	def process_response(self, response_data):
		""" make dictionary of data which are going to insert db using GoogleAPIReponse class"""

		try:
			list_data = []
			for ele in response_data.results :
				c = (str(ele['formatted_address']),str(ele['geometry']),str(ele['icon']),str(ele['id']),str(ele['name']),str(ele['place_id']), str(ele['rating']) if 'rating' in ele.keys() else '',str(ele['reference']),str(ele['types']), str(ele['photos']) if 'photos' in ele.keys() else '',self.TEXT_SEARCH_API_URL)
				list_data.append(c)
			if list_data :
				Application.insert_mass_data(Application.INSERT_QUERY, list_data)
		except Exception as ex:
			raise Exception(str(ex))
		
	def insert_mass_data(query, query_data):
		""" Make call to insert bulk data"""

		connector = DBConnector('',"SoftCmpyInfoDB.db")
		conn = connector.create_schema()
		db_cmt = DBManipulation(conn)
		db_cmt.many_insert_query_executor(query, query_data)

	def create_table(tableString):
		connector = DBConnector('',"SoftCmpyInfoDB.db")
		conn = connector.create_schema()
		db_cmt = DBManipulation(conn)
		db_cmt.create_table(tableString)
	
if __name__ == "__main__" :
	isNeedTable = sys.argv[1]
	if isNeedTable == '1':
		Application.create_table(Application.CREATE_TABLE_QUERY)
	application = Application(Application.GOOGLE_API_KEY)
	res_data = application.make_api_search([], None)
	print(' Data process finished ')
