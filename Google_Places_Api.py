
# GOOGLE PLACES API
# Google Cloud Platform
# julian.valdman123@gmail.com

import requests, json, time

class GooglePlaces(object):

	def __init__(self, api_key):
		super(GooglePlaces, self).__init__()
		self.api_key = api_key

	def search_places_by_coordinate(self, location, radius, types):
		endpoint_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
		places = []

		params = { 
			'location' : 	location,
			'radius' :		radius,
			# 'rankby' :		"distance",
			'types' :		types,
			'key' :			self.api_key
		}

		# res = requests.get(endpoint_url, params = params)
		res = requests.get(endpoint_url, params = params)
		results = json.loads(res.content)

		places.extend(results['results'])
		time.sleep(2)

		while 'next_page_token' in results:
			params['page_token'] = results['next_page_token']
			res = requests.get(endpoint_url, params = params)
			results = json.loads(res.content)
			places.extend(results['results'])
			time.sleep(2)

		return places

	def get_place_details(self, place_id, fields):
		endpoint_url = "https://maps.googleapis.com/maps/api/place/details/json"
		params = {
			'placeid' : 	place_id,
			'fields' :		",".join(fields),		# expects parameter to be a list: here comma, seperates it
			'key' :			self.api_key	
		}
		res = requests.get(endpoint_url, params = params)
		place_details = json.loads(res.content)
		return place_details


if __name__ == "__main__":

	api_key = 'AIzaSyAdq7_kYa5fkR0lWNLvHRT63gsa6cVUJxw'
	api = GooglePlaces(api_key) 

	inputs = { 
		'location' : "55.6754783,12.4631802",
		'radius' : 	'1000',
		# 'type' :	'restaurant',
		'type' :	'supermarket',
		'fields' : 	['name', 'formatted_address', 'international_phone_number', 'website', 'review', 'geometry', 'vicinity','utc_offset', 'price_level', 'rating']
	}

	places = api.search_places_by_coordinate(inputs['location'], inputs['radius'], inputs['type'])
	# print(places)

	for place in places:

		details = api.get_place_details(place['place_id'], inputs['fields'])

		# print(json.dumps(details, indent = 4))
		# print(json.dumps(place, indent = 4))

		try: user_ratings_total = place['user_ratings_total']
		except KeyError: user_ratings_total = ""

		try: website = details['result']['website']
		except KeyError: website = ""

		try: name = details['result']['name']
		except KeyError: name = ""

		try: address = details['result']['formatted_address']
		except KeyError: address = ""

		try: reviews = details['result']['reviews']
		except KeyError: reviews = []

		try:  location= details['result']['geometry']['location']
		except KeyError: location = ""
		
		try:  viewport= details['result']['geometry']['viewport']
		except KeyError: viewport = ""
		
		try:  vicinity= details['result']['vicinity']
		except KeyError: vicinity = ""
		
		try: utc_offset = details['result']['utc_offset']
		except KeyError: utc_offset  = ""

		try: price_level = details['result']['price_level']
		except KeyError: price_level = ""

		try: rating_1 = details['result']['rating']
		except KeyError: rating_1= ""


		print("\n-------- PLACE ----------")
		print(f"Name: {name}")
		print(f"Website: {website}")
		print(f"Address: {address}")
		print(f"Rating: {rating_1}")
		print(f"Rating count: {user_ratings_total}")
		print(f"Location: {location}")
		print(f"Viewport: {viewport}")
		print(f"Viewport: {viewport}")
		print(f"UTC Offset: {utc_offset} minutes")
		print(f"Price Level: {price_level}")
		print()

		for review in reviews:
			rating = review['rating']
			print(f"Rating: {rating}")

		print("-------------------------")
