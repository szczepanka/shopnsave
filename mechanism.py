#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  4 12:50:08 2020

@author: roopeilmola
"""

import pandas as pd
import numpy as np
mydataset = pd.read_csv('products.csv')



# Delete irrelevant columns for the user from the dataframe
mydataset = mydataset.drop(["startTime","store id","currency", "lastUpdate", "stock", "stockUnit"], axis=1)

# remove whitespace from column names 
mydataset.rename(columns={'store brand':'store_brand',
                          'store name':'store_name',
                          'store zip':'store_zip'}, 
                 inplace=True)


#filter products that fulfill a given zip code condition and export result to an excel file 
def product_filter (zipcode):
    search = (mydataset['store_zip']==zipcode)
    show_products = (mydataset[search])
    show_products.to_excel(r'Path where you want to store the exported excel file\File Name.xlsx', index = False)

product_filter(1958)
    

    
