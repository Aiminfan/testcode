# -*- coding: utf-8 -*-
"""
Created on Fri May 24 11:51:40 2019
Run this in commandline like:
    $Python run.py
    and you show be able to open 
    http://127.0.0.1:5000/Address
@author: aimin.fan
"""
from eve import Eve
app = Eve()

if __name__ == '__main__':
    app.run()