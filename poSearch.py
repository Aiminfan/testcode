# -*- coding: utf-8 -*-
"""
Created on Tue May 21 13:27:19 2019

@author: aimin.fan
"""
from geopy.geocoders import Nominatim
from geopy.geocoders import GeoNames
from geopy.geocoders import Here
from geopy.geocoders import TomTom
from geopy.geocoders import OpenMapQuest
from geopy.geocoders import Photon
from geopy.geocoders import GoogleV3
from geopy import distance

from pymongo import MongoClient
import re,json
import pprint
from bson.son import SON

def getreEx(flpth='data.json'):
    with open(flpth) as json_file:  
        data = json.load(json_file)
        return data
    return None
#print(data['CA']) #Output 3.5
#reCountry= json.loads(open(r'C:\afan\code\fBestAddress\postalcodeFormat.json'))
#print(reCountry)
def getPostal(address,country='CA'):
    reEx=getreEx()
    test = re.compile(reEx[country])
    #addr = '12345-67 Ave, Edmonton, AB T1A 2B3, Canada'
    r=test.search(address)
    p=''
    if r:
        p=r.group().replace(" ", "")
        return p
    return None
def checkMatchLevel(str1,str2):
    if len(str1)==len(str2)==6:
        for i in range(3):
            if str1[i]!=str2[i]:
                return i
    return -1    
            
if __name__ == '__main__':
    client = MongoClient()
    db = client['dbGIS']
    collection = db['Address']
    ptAddr=collection.find_one()
    pprint.pprint(ptAddr)
    addr=ptAddr['attributes']['ADDRESS']
    pt=(ptAddr['geometry']['y'],ptAddr['geometry']['x'])
    po=getPostal(addr)
    query = {"geometry": SON([("$nearSphere", ptAddr['geometry']), ("$maxDistance", 1)])}
    for doc in db['PostalCode'].find(query).limit(3):
        #print(doc)
        pt2=(doc['geometry']['coordinates'][1],doc['geometry']['coordinates'][0])
        accurate=distance.great_circle(pt, pt2).m
        
        po2=doc["properties"]["PostalCode"]
        #pprint.pprint(po2)
        m=checkMatchLevel(po,po2)
        print('first {} letters match, distance={}.'.format(m,accurate))