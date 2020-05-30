
# API Salling Group
# !!! GENEREL STUFF FOR THESE APIS (Used in every call)

import requests, json
import pandas as pd
import numpy as np

bearer_token = 'd300bde8-c38c-4d12-b9b0-2ef6732f72b2'
headers = { 'Authorization' : 'Bearer %s' % bearer_token }


# --------

# API 1

# API CALL: Stores and Food Waste with ZIP code
# Query with zip code as parameter to get stores in city and their food waste offers


def food_waste_offers_api(zip:int):

	url = 'https://api.sallinggroup.com/v1/food-waste/?'

	params = { 'zip' : zip }

	try:
		response = requests.get(url, params = params, headers = headers)
		data_dict_list = json.loads(response.content)
		return data_dict_list
	except:
		return "Error in zip code api data extraction"

	# !!! Remove # to see output
	# print(response.text)


# INVOCATION
# food_waste_offers_api()


# --------

# API 2

# API CALL: Suggested Products
# Query with product description as parameter to get suggested products to this initial search

# So we use "SUGGESTED PRODUCTS" and use description obtained from Food Waste Call
# So now we can find the product, and get product ID and more

def suggested_products_api():

	url_suggested_products = 'https://api.sallinggroup.com/v1-beta/product-suggestions/relevant-products?'

	params = { 'query' : 'GRÆSK FLADBRØD DELPANE' }

	response = requests.get(url_suggested_products, params = params, headers = headers)
	data_dict_list = json.loads(response.content)

	# !!! Remove # to see output
	#print(response.text)

	return data_dict_list

# INVOCATION
# suggested_products_api()



# --------

# API 3

# API CALL: Similar Products
# Query with productID as parameter to get similar products to this initial product


def similar_products_api():

	url_similar_products = 'https://api.sallinggroup.com/v1-beta/product-suggestions/similar-products?'

	params = { 'productId' : 5701205005559 }

	response = requests.get(url_similar_products, params = params, headers = headers)
	data_dict_list = json.loads(response.content)

	# !!! Remove # to see output
	# print(response.text)

	return data_dict_list

# INVOCATION
# similar_products_api()

# ---------

# API 4 

# API CALL: All Stores
# Query

def get_stores():

	url_stores = 'https://api.sallinggroup.com/v2/stores'

	params = { 'per_page' : 1500 }		# 1484 stores in total

	response = requests.get(url_stores, params = params, headers = headers)
	data_dict_list = json.loads(response.content)

	return data_dict_list


def get_zip_list():

	stores = get_stores()
	zips = []

	for store in stores:
		zipCode = store['address']['zip']
		if store['address']['country'] == 'DK':
			if zipCode not in zips:
				zips.append(zipCode)

	return zips
