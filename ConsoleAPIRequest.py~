"""
The wrapper class work arount Google Map APIs

@author Ideas2it
"""

import json
from decimal import Decimal

try:
    import six
    from six.moves import urllib
except ImportError:
    pass

from GoogleAPIError import GoogleAPIError
from GoogleAPIResponse import GoogleAPIResponse

class ConsoleAPIRequest(object):
	
	BASE_URL = 'https://maps.googleapis.com/maps/api'
	GEOCODE_API_URL = BASE_URL + '/geocode/json?'

	RESPONSE_STATUS_OK = 'OK'
	RESPONSE_STATUS_ZERO_RESULTS = 'ZERO_RESULTS' 

	def __init__(self, api_key):
		self._api_key = api_key
		self._request_params = None

	def company_search(self, service_url, query=None, lat_lng=None, location=None, pagetoken=None):
		""" Setup request params and validate its are correct"""

		self._request_params = {'query': query}
		if lat_lng is not None or location is not None:
            		lat_lng_str = self.generate_lat_lng_string(lat_lng, location)
            		self._request_params['location'] = lat_lng_str
		if pagetoken is not None:
            		self._request_params['pagetoken'] = pagetoken
		self.add_required_param_keys()
		url, response = self.fetch_remote_json(service_url, self._request_params)
		self.validate_response(url, response)
		return GoogleAPIResponse(self, response)

	def geocode_location(self, location, sensor=False):
		""" Make Google geo API call and get the lat, lng value
		and return as dict values			
		"""

		url, geo_response = self.fetch_remote_json(self.GEOCODE_API_URL,{'address': location, 'sensor': str(sensor).lower()})
		self.validate_response(url, geo_response)
		if geo_response['status'] == self.RESPONSE_STATUS_ZERO_RESULTS:
			error_detail = ('Lat/Lng for location \'%s\' can\'t be determined.' %                  location)
			raise GoogleAPIError(error_detail)
		return geo_response['results'][0]['geometry']['location']

	def fetch_remote_json(self, service_url, params=None, use_http_post=False):
		""" Getting JSON object from the URL """

		if not params:
			params = {}
		request_url, response = self.fetch_remote(service_url, params, use_http_post)
		str_response = response.read().decode('utf-8')
		return (request_url, json.loads(str_response, parse_float=Decimal))

	def fetch_remote(self, service_url, params=None, use_http_post=False):
		""" Retrieves a response from URL and return as duples """

		if not params:
			params = {}

		encoded_data = {}
		for k, v in params.items():
			if isinstance(v, six.string_types):
				v = v.encode('utf-8')
			encoded_data[k] = v
		encoded_data = urllib.parse.urlencode(encoded_data)

		if not use_http_post:
			query_url = (service_url if service_url.endswith('?') else '%s?' % service_url)
			request_url = query_url + encoded_data
			request = urllib.request.Request(request_url)
		else:
			request_url = service_url
			request = urllib.request.Request(service_url, data=encoded_data)
		return (request_url, urllib.request.urlopen(request, timeout = 6))

	def validate_response(self, url, response):
		""" Validate the reponse was from Google API""" 

		if response['status'] not in [self.RESPONSE_STATUS_OK, self.RESPONSE_STATUS_ZERO_RESULTS]:
			error_detail = ('Request to URL %s failed with response code: %s' %(url, response['status']))
			raise GoogleAPIError(error_detail)

	def generate_lat_lng_string(self, lat_lng, location):
		try:
			return '%(lat)s,%(lng)s' % (lat_lng if lat_lng is not None else geocode_location(location))
		except:
			raise ValueError('lat_lng must be a dict with the keys, \'lat\' and \'lng\'')
	
	def add_required_param_keys(self):
		self._request_params['key'] = self.api_key

	@property
	def request_params(self):
		return self._request_params

	@property
	def api_key(self):
		return self._api_key
