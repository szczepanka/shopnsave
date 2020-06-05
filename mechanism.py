#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  4 12:50:08 2020

@author: roopeilmola
"""

import pandas as pd
import numpy as np
from datetime import date
import datetime

from SallingGroup_Api import similar_products_api

mydataset = pd.read_csv('products.csv')

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

		# print(key, value)

		# search = (mydataset['store_zip']==zipcode)
		# show_products = (mydataset[search])

		if key == "percentDiscount": 
			products = products[products[key] >= value]
		else:
			# print(products)
			products = products[products[key]==value]
			# print("AFTER:", products)

	products['endTime'] = products['endTime'].apply(lambda x: datetime.datetime.strptime(x[:10], '%Y-%m-%d')) 
	print(products['endTime'])

	today = date.today()
	products = products[products['endTime'] >= today]

	print("hej", similar_products_api(5712580738598))

	print(products)

	# show_products = (mydataset[search])
	# show_products.to_excel(r'MechanismOutput.xlsx', index = False)


# product_filter(1958)
product_filter(filterParameterDict)
    

    
