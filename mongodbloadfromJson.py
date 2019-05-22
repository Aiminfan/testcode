# -*- coding: utf-8 -*-
"""
Created on Wed May 22 10:45:36 2019

@author: aimin.fan
"""

import json
from pymongo import MongoClient
from bson import json_util

client = MongoClient('localhost', 27017)
db = client['dbGIS']
collection_c = db['CountryCode']

with open(r'E:\myfiles\fnProjects\country-codes_json.json') as f:
    file_data = json.load(f)
    jArray = json.dumps(file_data, default=json_util.default)

# use collection_currency.insert(file_data) if pymongo version < 3.0
    collection_c.insert_many(file_data)  
    client.close()
    
