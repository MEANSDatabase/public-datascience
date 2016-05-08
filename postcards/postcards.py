# -*- coding: utf-8 -*-
"""
Created on Thu May  5 13:45:44 2016

@author: grant
"""

# Expected output: Ordered list of zip codes to focus on for post cards. 
# Expected output: Guess for which postcard type (A, B) to send to each zip code

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# %matplotlib # magic command for iPython

postcards = pd.read_csv('data/postcards_feb2016.csv')


# Define feature cols 
relevant_cols = [
    'latitude',
    'longitude',
    'postcard_design',
    'handwritten_address',
    'returned',
    'means_user'
]

# drop columns we don't care about. 
for column in postcards.columns:    
    if column not in relevant_cols:
        postcards.drop(column, 1, inplace=True)

postcards['design_a'] = postcards.postcard_design == 'A'
postcards['design_b'] = postcards.postcard_design == 'B'
postcards['means_user'] = postcards.means_user == True 

# Drop non-integer 
postcards.drop("postcard_design", 1, inplace=True)

# Define feature cols 
feature_cols = [
    'latitude',
    'longitude',
    #'zipcode',
    'returned',
    'design_a',
    'design_b',
    'handwritten_address'
]


# Some data viz. 
corr = postcards.corr() 
#sns.heatmap(corr) # lol basically latitude is the best indicator :( 


# Do it without latitude/longitude. 
no_geo = postcards
no_geo.drop("latitude", 1, inplace=True)
no_geo.drop("longitude", 1, inplace=True)
corr = no_geo.corr()
#sns.heatmap(corr)

non_returned = postcards[postcards.returned != True]
non_returned.drop("returned", 1, inpace=True)
non_returned_corr = non_returned.corr()
# sns.heatmap(non_returned_corr)

design_columns = ["design_a", "design_b", "means_user"]
design_test = pd.DataFrame(non_returned, columns=design_columns)
design_test = design_test[design_test.means_user == True]
sns.heatmap(design_test.corr())



# FYI. 
reponse_col = ['means_user']



# Try logistic regression 
# Something isn't right w/ this approach. zips? longitude scaling? 
from sklearn.linear_model import LogisticRegression

logreg = LogisticRegression() 
X = postcards[feature_cols]
y = postcards.means_user

logreg.fit(X, y)

postcards['means_prediction_class'] = logreg.predict(X)
postcards.head() 


# Try linear regression.
# Something isn't right
from sklearn.linear_model import LinearRegression

linreg = LinearRegression() 
X = postcards[feature_cols]
y = postcards.means_user

linreg.fit(X, y)

postcards['means_prediction_linear'] = linreg.predict(X)
postcards.head() 



