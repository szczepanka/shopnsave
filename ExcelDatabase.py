
# EXCEL DATABASE MANAGEMENT

import pandas as pd
from SallingGroup_Api import food_waste_offers_api, get_zip_list
import time

# IMPORT STATEMENT EXPLANATION:
# from the file "SallingGroup_Api.py" the script import the function "food_waste_offers_api" from this file
# So now we can call this function in THIS script as well
# This structures the files, so it makes a better overview since this file is only about functions related to Excel


# Export to EXCEL

def export_api_data_to_csv(api_data):

	try:
		if 'code' in api_data.keys():
			print("Invalid Zip")
			return

		elif api_data['statusCode'] == 429:
			print("Limit reached: blocked by API")
			return

	except Exception as e: ()

	try: 
		existingData = pd.read_csv("products.csv")
		existingData['ean'] = existingData['ean'].apply(lambda x: str(x))		# convert ean column to all be string formatted
		existingData = existingData.set_index('ean')

	except FileNotFoundError as e:
		existingData = pd.DataFrame()
		print("No existing data found")

	except PermissionError as e:
		print("products.csv file open, it cannot be accessed")
		return

	# else:
	# 	print("Something went wrong..")
	# 	return

	# print(api_data)

	product_dict = {}

	# if not isinstance(api_data, list): api_data = [api_data] 

	for storeItem in api_data:

		for productItem in storeItem['clearances']:
			
			product_key = str(productItem['offer']['ean'])

			product_dict[product_key] = productItem['offer']
			product_dict[product_key]['store brand'] = storeItem['store']['brand']
			product_dict[product_key]['store name'] = storeItem['store']['name']
			product_dict[product_key]['store id'] = storeItem['store']['id']
			product_dict[product_key]['store zip'] = storeItem['store']['address']['zip']

			# print(storeItem['store'])
		
	products_df = pd.DataFrame.from_dict(product_dict, orient='index')

	if not products_df.empty: products_df = products_df.set_index('ean')	

	# print("\n\n", product_dict)
	# print(products_df)

	products_acc = existingData.append(products_df)
	# print("Exi:", existingData.shape)
	# print("Acc:", products_acc.shape)

	products_acc = products_acc.loc[~products_acc.index.duplicated(keep='last')]  	# takes the last occurence if duplicated

	# print(products_acc.shape)
	print(f"{products_acc.shape[0] - existingData.shape[0]} lines added to the Excel Database since last run")
	print(f"{products_acc.shape[0]} records in the Excel Database now")
	products_acc.to_csv("products.csv")
	return

def update_all_stores():

	zipList = get_zip_list()

	for zip in zipList:

		time.sleep(2)

		print(f'{zip}:')
		dictData = food_waste_offers_api(zip)
		# print(dictData)
		if dictData == "Error in zip code api data extraction": 
			continue
		export_api_data_to_csv(dictData)


if __name__ == '__main__':

	# export_api_data_to_csv(food_waste_offers_api(2000))
	# food_waste_offers_api(8000)
	update_all_stores()