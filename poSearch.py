# -*- coding: utf-8 -*-
"""
Created on Tue May 21 13:27:19 2019

@author: aimin.fan
"""
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
if __name__ == '__main__':
    client = MongoClient()
    db = client['dbGIS']
    collection = db['Address']
    ptAddr=collection.find_one()
    pprint.pprint(ptAddr)
    addr=ptAddr['attributes']['ADDRESS']
    print(addr)
    query = {"geometry": SON([("$nearSphere", ptAddr['geometry']), ("$maxDistance", 100)])}
    for doc in db['PostalCode'].find(query).limit(3):
        pprint.pprint(doc)