#Primary Account Key 	fEDnzx4E0/mMUwHi3KPfXkznrQ14JLzTiNcR1XQwi/s
#Customer ID 	d7a4a396-67f1-4135-9ade-969b0bfd6af3
#firstwenwen@outlook.com
#zww19871130


import requests # Get from https://github.com/kennethreitz/requests
import string
import json
import vision

class BingSearchAPI():

	# bing_url = "https://api.datamarket.azure.com/Data.ashx/Bing/Search/v1/Image?"
	bing_url = "https://api.datamarket.azure.com/Bing/Search/v1/Image"
	
	def __init__(self, key):
		self.key = key

	def replace_symbols(self, request):
		# Custom urlencoder.
		# They specifically want %27 as the quotation which is a single quote '
		# We're going to map both ' and " to %27 to make it more python-esque
		request = request.replace("'", '%27')
		request = request.replace('"', '%27')
		request = request.replace('+', '%2b')
		request = request.replace(' ', '%20')
		request = request.replace(':', '%3a')
		return request
		
	def search(self, sources, query, params):
		''' This function expects a dictionary of query parameters and values.
			Sources and Query are mandatory fields. 
			Sources is required to be the first parameter.
			Both Sources and Query requires single quotes surrounding it.
			All parameters are case sensitive. Go figure.
			For the Bing Search API schema, go to http://www.bing.com/developers/
			Click on Bing Search API. Then download the Bing API Schema Guide
			(which is oddly a word document file...pretty lame for a web api doc)
		'''

		# payload = {'$format': 'json', '$top': 10, '$skip': 0}

		params["Query"] = "'" + query.replace("+", " ") + "'"

		return requests.get(self.bing_url, params=params, auth=(self.key, self.key))

	  
def getBingResult(query):

	my_key = 'eX5lsVsUjnMG3WXaCerD+HygBmGtZM20SqmsBZTdBMU'
	bing = BingSearchAPI(my_key)
	params = {'$format': 'json', '$top': 10, '$skip': 0}
	response = bing.search('web', query, params).json()

	# print(json.dumps(response['d']['results']), '\n\n\n')

	return response['d']['results']
	

	
def getFirstImage(keyword):

	# get bing image results for a keyword
	results = getBingResult(keyword)
	# use the first image result from bing
	image_resource = results[0]

	# get the url from the response
	image_thumb_url = image_resource['Thumbnail']['MediaUrl']
	image_url = image_resource['MediaUrl']

	image = vision.readFromUrl(image_url)

	if image is None:
		image = vision.readFromUrl(image_thumb_url)

	return image