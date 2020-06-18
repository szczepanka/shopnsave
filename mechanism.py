#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  4 12:50:08 2020

@author: roopeilmola
"""

import pandas as pd
import numpy as np
from datetime import date
import datetime, time

from SallingGroup_Api import similar_products_api, suggested_products_api

mydataset = pd.read_csv('products.csv', index_col = 'ean')
userInput = pd.read_excel('UserInput.xlsx')
filterParameterDict = dict(zip(userInput.parameter, userInput.value))

# Delete irrelevant columns for the user from the dataframe
mydataset = mydataset.drop(["startTime","store id","currency", "lastUpdate", "stock", "stockUnit"], axis=1)

# remove whitespace from column names 
mydataset.rename(columns={'store brand':'store_brand',
                          'store name':'store_name',
                          'store zip':'store_zip'}, 
                 inplace=True)


#filter products that fulfill a given zip code condition and export result to an excel file 
def product_filter (filter_dict):

	products = mydataset

	for key, value in filter_dict.items():

		try:
			if key == "percentDiscount": 
				products = products[products[key] >= value]
			else:
				products = products[products[key]==value]
		except:
			continue

	products['endTime'] = products['endTime'].apply(lambda x: datetime.datetime.strptime(x[:10], '%Y-%m-%d')) 
	print(products['endTime'])

	today = date.today()
	products = products[products['endTime'] >= today]

	return products

def add_suggested_products(products_df):

	for index, item in products_df.head(5).iterrows():
		print(item)

		time.sleep(1)

		try:
			suggested_product = suggested_products_api(item['productDescription'])['suggestions'][0]
			products_df.loc[suggested_product['id'], 'originalPrice'] = suggested_product['price']
			products_df.loc[suggested_product['id'], 'productDescription'] = suggested_product['title']
			products_df.loc[suggested_product['id'], 'productID'] = suggested_product['prod_id']
			print(suggested_product)
		except: ()

	return products_df


if __name__ == "__main__":

	products = product_filter(filterParameterDict)
	products = add_suggested_products(products)

	# products.to_excel("MechanismOutput.xlsx")

	print(products)

    
