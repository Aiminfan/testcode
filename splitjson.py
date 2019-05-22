# -*- coding: utf-8 -*-
"""
Created on Wed May 22 12:25:01 2019

@author: aimin.fan
"""

import json
import sys
if len(sys.argv)>1:
    n=sys.argv[1]
else:
    n=r'E:\myfiles\fnProjects\address.geojson'
with open(n,'r') as infile:
    o = json.load(infile)
    chunkSize = 30000
    for i in range(0, len(o), chunkSize):
        with open(n.split('.')[0] + '_' + str(i//chunkSize) + '.geojson', 'w') as outfile:
            json.dump(o[i:i+chunkSize], outfile)