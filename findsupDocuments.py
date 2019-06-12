# -*- coding: utf-8 -*-
"""
Created on Wed May 29 12:58:54 2019

@author: aimin.fan
"""
import pandas as pd
from pymongo import MongoClient
from pandas.io.json import json_normalize

def _connect_mongo(host, port, username, password, db):
    """ A util for making a connection to mongo """

    if username and password:
        mongo_uri = 'mongodb://%s:%s@%s:%s/%s' % (username, password, host, port, db)
        conn = MongoClient(mongo_uri)
    else:
        conn = MongoClient(host, port)


    return conn[db]


def read_mongo(db, collection, query={}, host='localhost', port=27017, username=None, password=None, no_id=True):
    """ Read from Mongo and Store into DataFrame """

    # Connect to MongoDB
    db = _connect_mongo(host=host, port=port, username=username, password=password, db=db)

    # Make a query to the specific DB and Collection
    cursor = db[collection].find(query)

    # Expand the cursor and construct the DataFrame
    df =  pd.DataFrame(list(cursor))

    # Delete the _id
    if no_id:
        del df['_id']

    return df
#client = MongoClient()
#db = client['dbGIS']
#collection = db['Address']

#cursor = collection.aggregate(
#    [
#        {"$group": {"_id": "$ID", "unique_ids": {"$addToSet": "$_id"}, "count": {"$sum": 1}}},
#        {"$match": {"count": { "$gte": 2 }}}
#    ]
#)
dups=[]
found=[]
df=read_mongo('dbGIS', 'Address4')

# Select all duplicate rows based on multiple column names in list
duplicateRowsDF = df[df.duplicated(['Address'])]

for index, row in duplicateRowsDF.iterrows():
    print(row)



#collection.remove({"_id": {"$in": response}})