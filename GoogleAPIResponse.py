#!/usr/bin/python3

class GoogleAPIResponse(object):
	def __init__(self, query_instance, response):
		self._response = response
		self._results = []
		for result in response['results']:
			self._results.append(result)
		self._html_attributions = response.get('html_attributions', [])
		self._next_page_token = response.get('next_page_token', [])

	@property
	def raw_response(self):
		return self._response
	
	@property
	def results(self):
		return self._results
	
	@property
	def html_attributions(self):
		return self._html_attributions
	
	@property
	def next_page_token(self):
		return self._next_page_token
	
	@property
	def has_attributions(self):
		return len(self.html_attributions) > 0
	
	@property
	def has_next_page_token(self):
		return len(self.next_page_token) > 0

	def __repr__(self):
		""" Return a string representation stating the number of results."""
		return '<{} with {} result(s)>'.format(self.__class__.__name__, len(self.results))
