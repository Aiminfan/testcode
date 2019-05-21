# -*- coding: utf-8 -*-
"""
Created on Fri May 17 08:07:28 2019
Find best available address/coordinate
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
#import pandas as pd
import os
import ogr, osr
#import time
import requests
def replacefileExtension(f,ext):
    if not ext.startswith('.'):
        ext='.'+ext
    return os.path.splitext(f)[0]+ext

def reprojectPoint(pt,frmEPSG=26917,toEPSG=4326):
    # create coordinate transformation
    inSpatialRef = osr.SpatialReference()
    inSpatialRef.ImportFromEPSG(frmEPSG)
    outSpatialRef = osr.SpatialReference()
    outSpatialRef.ImportFromEPSG(toEPSG)
    coordTransform = osr.CoordinateTransformation(inSpatialRef, outSpatialRef)
    # transform point
    pt.Transform(coordTransform)
    return pt #[point.GetX(), point.GetY()]
def reprojectXY(_x,_y,frmEPSG=26917,toEPSG=4326):
    # create a geometry from coordinates
    point = ogr.Geometry(ogr.wkbPoint)
    point.AddPoint(_x, _y)
    return reprojectPoint(point,frmEPSG,toEPSG)
def reprojectXYgetjson(_x,_y,frmEPSG=26917,toEPSG=4326):
    pt=reprojectXY(_x, _y,frmEPSG,toEPSG)
    return {'x':pt.GetX(), 'y':pt.GetY(),"spatialReference": {
        "wkid": toEPSG}}


def revGeocodingbyIQ(_lat,_lon):
    url = "https://us1.locationiq.com/v1/reverse.php"
    data = {'key': '91013ed0a98308','lat': '{}'.format(_lat),'lon': '{}'.format(_lon),'showdistance':'1','format': 'json'}

    addrDict={'Geocoder':'revGeocodingbyIQ','address':'','accuracy':999}
    try:
        response = requests.get(url, params=data)
        res=response.json()
        if 'display_name' in res:
             addrDict['address']= res['display_name']
        if 'distance' in res:
             addrDict['accuracy']= res['distance']
    except:
        print('reverse geocoding (revGeocodingbyIQ) filed:lat:{},Lon:{}'.format(_lat,_lon))
    finally:
        return addrDict
def revGeocodingGeopy(_lat,_lon,geolocator):
    listaddrs=[]
    addrDict={'Geocoder':geolocator['name'],'address':'','accuracy':999}
    try:
        gl=geolocator['locator']
        location = gl.reverse('{},{}'.format(_lat,_lon),exactly_one=False)
        if location:
            #if len(location)>0:
            for lc in location:
                print(lc)
                if len(lc)>0:
                    addrDict['address']=lc[0]
                    addrDict['accuracy']=getAccuracy(_lat,_lon,addrDict['address'],gl)
                    listaddrs.append(addrDict)
    except:
        print(geolocator['name'] , 'Exception!')
        return listaddrs
    return listaddrs
def getAccuracy(_lat,_lon,addr,geolocator):
    p1=(_lat,_lon)
    p2=getLatLon(addr,geolocator)
    if p2:
        d=distance.great_circle
        dv=d(p1,p2).m
        #print('{} m offset for address: {}'.format(dv,addr))
        return dv
    else:
        return 999
def getLatLon(addr,geolocator):
    l=geolocator.geocode(addr)
    if l:
        if len(l)>=2:
            return l[1]
    return None
def collectGeocoders():
    locators=[{'locator':Nominatim(user_agent="afan"),'name':'Nominatim','type':'Geopy'},
              {'locator':GeoNames(username="aimfan"),'name':'GeoNames','type':'Geopy'},
              {'locator':Here(app_id='crWSWbTEdtSHk8z9gf8n', app_code='kIeuGud2FxMyWk_rxn4zLg'),'name':'Here','type':'Geopy'},
              {'locator':TomTom(api_key='UVZplrrIv0chiLLV7R1E2HPZJdHOH6FZ'),'name':'TomTom','type':'Geopy'},
              {'locator':OpenMapQuest(api_key='hyIeA4pV5rPpORQzaGcGfckbMHpSnraG'),'name':'OpenMapQuest','type':'Geopy'},
              {'locator':Photon(),'name':'Photon','type':'Geopy'}
              ]
    #locators.append({'locator':GoogleV3(api_key='AIzaSyDSQOxaeImKa_gppD48Nt_wsdmqjGnFCmo'),'name':'GoogleV3','type':'Geopy'})
    locators.append({'locator':revGeocodingbyIQ,'name':'revGeocodingbyIQ','type':'Custom'})

    return locators
def getBestAddress(_lat,_lon):
    print('processing: Lon: {},Lat: {}'.format(_lon,_lat))
    locators=collectGeocoders()
    mindv=999
    bestAddr=None
    for l in locators:
        if l['type']=='Geopy':
            addrl=revGeocodingGeopy(_lat,_lon,l)
            addr=addrl[0]
        elif l['type']=='Custom':
            g=l['locator']
            addr=g(_lat,_lon)
        else:
            addr=None
            print('Geocoder {} Not Implemented!'.format(l['name']))
        if addr:
            fdv=998.9
            dv=addr['accuracy']
            if type(dv)==float or type(dv)==int:
                fdv=dv
            elif type(dv)==str:
                if dv.isdigit():
                    fdv=float(dv)
                else:
                    print('{} is not number!'.format(dv))
            else:
                print('{} not implemented'.format(type(dv)))
            if fdv < mindv:
                mindv=dv
                bestAddr=addr
    return bestAddr
def getBestLocation(addressString):
    print('processing:{}'.format(addressString))
    locators=collectGeocoders()
    for l in locators:
        addrDict={'Geocoder':l['name'],'address':addressString,'location':None,'accuracy':999}
        if l['type']=='Geopy':
            try:
                gl=l['locator']
                location = gl.geocode('{}'.format(addressString),exactly_one=False)
                if len(location)>0:
                    
                    if len(location[0])>0:
                        addrDict['location']=location[0][1]
                    return addrDict
            except:
                print('Error when geocoding!')
                continue
    return None

def getAllAddress(_lat,_lon):
    print('processing: Lon: {},Lat: {}'.format(_lon,_lat))
    locators=collectGeocoders()
    lAddr=[]
    for l in locators:
        if l['type']=='Geopy':
            addr=revGeocodingGeopy(_lat,_lon,l)
            lAddr=lAddr+addr
        elif l['type']=='Custom':
            g=l['locator']
            addr=g(_lat,_lon)
            lAddr.append(addr)
        else:
            addr=None
            print('Geocoder {} Not Implemented!'.format(l['name']))
    return lAddr
if __name__ == '__main__':
    #originaddress='320 Queen St. Chatham ON'
    originaddress='36 Birmingham Ln. Chatham ON'
    b=getBestLocation(originaddress)
    print(b['location'],'\n\n')
    a=getAllAddress(b['location'][0], b['location'][1])
#    print(a)
    for item in a:
        
        print(item)