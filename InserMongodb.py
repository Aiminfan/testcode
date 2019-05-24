# -*- coding: utf-8 -*-
"""
Created on Thu May 23 08:27:42 2019

@author: aimin.fan
"""
#Use upsert option:
from pymongo import MongoClient
from pymongo import TEXT,GEOSPHERE
from bson.son import SON
from geopy.geocoders import Nominatim
from geopy.geocoders import GeoNames
from geopy.geocoders import Here
from geopy.geocoders import TomTom
from geopy.geocoders import OpenMapQuest
from geopy.geocoders import Photon
from geopy.geocoders import GoogleV3
from geopy import distance

client = MongoClient()
db = client['dbGIS']
collection = db['Address']

collection.create_index([("geometry", GEOSPHERE)])
#collection.create_index([('attributes.Address',TEXT)])
#myquery = { "attributes.ADDRESS": { "$regex": "^39316-40298 Bush Line" } }
#myquery = { "attributes.FID": { "$lt": 10 } }
myquery = { "attributes.ADDRESS": '39316-40298 Bush Line, St Thomas, Ontario, N5P 3S9' }

ptAddr=collection.find(myquery)
for x in ptAddr:
  print('l1',x)
  #squery={"geometry": SON([("$nearSphere", x['geometry']), ("$maxDistance", 0.00001)])}
  #squery={"geometry" : SON([("$nearSphere", x['geometry'])])}
  q1={"geometry" : SON([("$nearSphere", x['geometry'])])} #search near
  q2={'_id':{"$ne": x['_id']}} #not include itself
  squery={"$and":[q1,q2]}
  tAddr=collection.find(squery).limit(3)
  for y in tAddr:
      print('l2:')
      p1=(x['geometry']['y'],x['geometry']['x'])
      p2=(y['geometry']['y'],y['geometry']['x'])
      dv=distance.great_circle(p1,p2).m
      print('distance:{}(m)'.format(dv))
  
#data = [{"attributes":{"FID":-1,"ADDRESS":"320 Queen St. Chatham ON"},"geometry":{"x":-82.3788485244898,"y":42.5918194183674},"Precision":1,"Accuracy":-1,"MatchLevel":0}]
#for d in data:
#    x=collection.update({"attributes.ADDRESS":d['attributes']['ADDRESS']}, d, True)
#    print(x)