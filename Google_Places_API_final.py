# GOOGLE PLACES API for Shop'n'Save
# Google Cloud Platform
# adkr19ad@students.cbs.dk

import requests, json, time, openpyxl
import pandas as pd

class GooglePlaces(object):

    def __init__(self, api_key):
        super(GooglePlaces, self).__init__()
        self.api_key = api_key

    def turn_address_into_coordinates(self, location):
        endpoint_url = "https://maps.googleapis.com/maps/api/geocode/json?"

        params = {
            'key' : self.api_key,
            'address' : location
        }
        res = requests.get(endpoint_url, params = params)
        addresscoordinates = json.loads(res.content)

        lat = addresscoordinates['results'][0]['geometry']['location']['lat']
        lng = addresscoordinates['results'][0]['geometry']['location']['lng']

        return lat, lng

    def search_places_by_coordinates(self, location, radius, types, store_brand):
        # endpoint_url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location[0]},{location[1]}&radius={radius}&type={types}&key={self.api_key}"
        # url="https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=-33.8670522,151.1957362&radius=1500&type=restaurant&keyword=cruise&key=" + self.api_key #THAT IS NOT NEEDED, IS IT?

        endpoint_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"

        places = []

        params = {
            'key' :	self.api_key,
            'location' : 	f"{location[0]},{location[1]}",
            'radius' :		radius,
            'type' :		types,
            'keyword' :     store_brand
        }
        res = requests.get(endpoint_url, params = params) 

        results = json.loads(res.content)
        places.extend(results['results'])
        time.sleep(1)

        # while 'next_page_token' in results:

        #     params['page_token'] = results['next_page_token']
        #     res = requests.get(endpoint_url, params = params)
        #     results = json.loads(res.content)

        #     print(results)
        #     places.extend(results['results'])
        #     time.sleep(2)

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

    def getStoresDataFrame(self, coordinates : tuple, store_brands = ['Netto', 'Føtex', 'Bilka']):

        stores_df = pd.DataFrame()

        for store_brand in store_brands:

            stores = api_coordinates.search_places_by_coordinates(coordinates, inputs['radius'], inputs['type'], store_brand = store_brand)

            for store in stores:
                stores_df.loc[store['place_id'], 'brand'] = store['name']
                stores_df.loc[store['place_id'], 'address'] = store['vicinity']
                stores_df.loc[store['place_id'], 'rating'] = store['rating']

        print(stores_df)
        return stores_df


if __name__ == "__main__":

    api_key1 = 'AIzaSyBb36Kwn6O9hvs6fNZ0TgjLuzvnKnqoiko'
    api_key2 = 'AIzaSyAdq7_kYa5fkR0lWNLvHRT63gsa6cVUJxw'
    api_coordinates = GooglePlaces(api_key1) 
    api_nearby_details = GooglePlaces(api_key2) 

    userInput = pd.read_excel('UserInput.xlsx')
    filterParameterDict = dict(zip(userInput.parameter, userInput.value))

    inputs = { 
        'location'      : '',
        'radius'        : '',
        'store_brand'   : '',
        'type'          : 'supermarket'
    }
    try:
        inputs['location'] = filterParameterDict['address']
        inputs['radius'] = filterParameterDict['radius']
        inputs['store_brand'] = filterParameterDict['store_brand']

        coordinates = api_coordinates.turn_address_into_coordinates(inputs['location'])

        stores = api_coordinates.getStoresDataFrame(coordinates = coordinates, store_brands = [ inputs['store_brand'] ])
        stores.to_excel("StoresNearby.xlsx")

    except: print("fejl")

'''
    for place in places:

        details = api_nearby_details.get_place_details(place['place_id'], inputs['fields'])

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
        '''