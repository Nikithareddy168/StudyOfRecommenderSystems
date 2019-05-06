#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  6 22:42:31 2019

@author: chichhil
"""

	
import pandas as pd
import numpy as np
 
# Load Training Data
data_raw = pd.read_csv(
        'review_with_city.csv',
        usecols=['user_id', 'business_id', 'stars'],
        dtype = {'user_id': str, 'business_id': str, 'stars': np.int})

 
# Extract the k-core
k = 50
done = False
while ~done :
    print "ping {}".format(data_raw.shape[0])
    countRatingsASIN = data_raw.groupby(['business_id'])['stars'].count()
    countRatingsUser = data_raw.groupby(['user_id'])['stars'].count()
 
    mask = []
    done = True
    for idx, x in data_raw.iterrows() :
        if (idx/100000 > (idx-1)/100000) : print "{}/{}".format(idx,data_raw.shape[0])
        cur = (countRatingsASIN[x['business_id']] >= k) & (countRatingsUser[x['user_id']] >= k)
        done = done & cur
        mask.append(cur)
    print "pong"
    data_raw = data_raw[mask]
    if data_raw.shape[0] == 0:
        break


data_raw
data_raw.to_csv("Business_Ratings.csv",index = False)
