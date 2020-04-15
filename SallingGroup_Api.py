
# API Salling Group

# !!! GENEREL STUFF FOR THESE APIS (Used in every call)

import requests, json

bearer_token = 'd300bde8-c38c-4d12-b9b0-2ef6732f72b2'
headers = { 'Authorization' : 'Bearer %s' % bearer_token }


# --------

# API 1

# API CALL: Stores and Food Waste with ZIP code
# Query with zip code as parameter to get stores in city and their food waste offers

url = 'https://api.sallinggroup.com/v1/food-waste/da2957d5-67ec-4f24-9c49-235b6712e063?'

params = { 'zip' : 2000 }

response = requests.get(url, params = params, headers = headers)
data_dict = json.loads(response.content)

# !!! Remove # to see output
# print(response.text)





# --------

# API 2

# API CALL: Suggested Products
# Query with product description as parameter to get suggested products to this initial search

# So we use "SUGGESTED PRODUCTS" and use description obtained from Food Waste Call
# So now we can find the product, and get product ID and more

url_suggested_products = 'https://api.sallinggroup.com/v1-beta/product-suggestions/relevant-products?'

params = { 'query' : 'GRÆSK FLADBRØD DELPANE' }

response = requests.get(url_suggested_products, params = params, headers = headers)
data_dict = json.loads(response.content)


# !!! Remove # to see output
#print(response.text)






# --------

# API 3

# API CALL: Similar Products
# Query with productID as parameter to get similar products to this initial product

url_similar_products = 'https://api.sallinggroup.com/v1-beta/product-suggestions/similar-products?'

params = { 'productId' : 5701205005559 }

response = requests.get(url_similar_products, params = params, headers = headers)
data_dict = json.loads(response.content)

# !!! Remove # to see output
# print(response.text)
