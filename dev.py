# -*- coding: utf-8 -*-
"""
Created on Thu May 16 11:09:01 2019

@author: aimin.fan
"""
import pandas as pd
import os
if __name__ == '__main__':
    path_base='C:\Projects\RevGeocoding_report'
    inputpath=os.path.join(path_base,'input')
    outputpath=os.path.join(path_base,'report\Switch.csv')
    files = [os.path.join(inputpath,f) for f in os.listdir(inputpath) if os.path.isfile(os.path.join(inputpath,f))]
    dflist=[]
    for f in files:
        if f.endswith('.xls'):
            df=pd.read_excel(f)
        elif f.endswith('.xlsx'):
            df=pd.read_excel(f)
        elif  f.endswith('.csv'):
            df=pd.read_csv(f)
        dflist.append(df)
    result = pd.concat(dflist) 
    result.to_csv(outputpath,index=False)
      