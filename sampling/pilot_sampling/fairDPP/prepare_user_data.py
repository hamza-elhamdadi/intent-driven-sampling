import os,sys

import utils as ut
import numpy as np
import pandas as pd
from random import seed, shuffle
#SEED = 1122334455
#seed(SEED) # set the random seed so that the random permutations can be reproduced again
#np.random.seed(SEED)

"""
    The adult dataset can be obtained from: http://archive.ics.uci.edu/ml/datasets/Adult
    The code will look for the data files (adult.data, adult.test) in the present directory, if they are not found, it will download them from UCI archive.
"""

def check_data_file(fname):
    files = os.listdir(".") # get the current directory listing
    print("Looking for file '%s' in the current directory..." % fname)

    if fname not in files:
        print("'%s' not found! Downloading from UCI Archive..." % fname)
        
    else:
        print("File found in current directory..")
    
    print('')
    return

def load_user_data(load_data_size=None):

    """
        if load_data_size is set to None (or if no argument is provided), then we load and return the whole data
        if it is a number, say 10000, then we will return randomly selected 10K examples
    """

    attrs = ['country', 'socialNbFollowers', 'socialNbFollows', 'socialProductsLiked',\
             'productsListed', 'productsSold', 'productsPassRate', 'productsWished', 'productsBought',\
             'gender', 'hasAnyApp', 'hasAndroidApp', 'hasIosApp', 'hasProfilePicture',\
             'daysSinceLastLogin', 'seniority'] # attributes with integer values -- the rest are categorical
    int_attrs = ['socialNbFollowers', 'socialNbFollows', 'socialProductsLiked', 'productsListed',\
                 'productsSold', 'productsPassRate', 'productsWished', 'productsBought',\
                 'daysSinceLastLogin', 'seniority'] # attributes with integer values -- the rest are categorical
    sensitive_attrs = ['gender'] # the fairness constraints will be used for this feature
    attrs_to_ignore = ['gender'] # sex and race are sensitive feature so we will not use them in classification, we will not consider fnlwght for classification since its computed externally and it highly predictive for the class (for details, see documentation of the adult data)
    attrs_for_classification = set(attrs) - set(attrs_to_ignore)

    # adult data comes in two different files, one for training and one for testing, however, we will combine data from both the files
    data_files = ["data_final.csv"]



    X = []
    y = []
    x_control = {}

    attrs_to_vals = {} # will store the values for each attribute for all users
    for k in attrs:
        if k in sensitive_attrs:
            x_control[k] = []
        elif k in attrs_to_ignore:
            pass
        else:
            attrs_to_vals[k] = []

    for f in data_files:
        check_data_file(f)

        for line in open(f):
            line = line.strip()
            if line == "": continue # skip empty lines
            if line.startswith("country"): # ignore header
                continue
            line = line.split(",")
            line = line[:-3]
            
            y.append(1) #fixed class label because there isn't any

            for i in range(0,len(line)):
                attr_name = attrs[i]
                attr_val = line[i]

                if attr_name in sensitive_attrs:
                    x_control[attr_name].append(attr_val)
                elif attr_name in attrs_to_ignore:
                    pass
                else:
                    attrs_to_vals[attr_name].append(attr_val)
                    

    def convert_attrs_to_ints(d): # discretize the string attributes
        for attr_name, attr_vals in d.items():
            if attr_name in int_attrs: continue
            uniq_vals = sorted(list(set(attr_vals))) # get unique values

            # compute integer codes for the unique values
            val_dict = {}
            for i in range(0,len(uniq_vals)):
                val_dict[uniq_vals[i]] = i
            # replace the values with their integer encoding
            for i in range(0,len(attr_vals)):
                attr_vals[i] = val_dict[attr_vals[i]]
            d[attr_name] = attr_vals

    
    # convert the discrete values to their integer representations
    convert_attrs_to_ints(x_control)
    convert_attrs_to_ints(attrs_to_vals)
    

    # if the integer vals are not binary, we need to get one-hot encoding for them
    for attr_name in attrs_for_classification:
        attr_vals = attrs_to_vals[attr_name]
        if attr_name in int_attrs or attr_name in ['hasAnyApp', 'hasAndroidApp', 'hasIosApp',\
            'hasProfilePicture']: #MUST catch everything that is int or binary category, otherwise will fuck up
            X.append(attr_vals)

        else:            
            attr_vals, index_dict = ut.get_one_hot_encoding(attr_vals)
            for inner_col in attr_vals.T:                
                X.append(inner_col) 


    # convert to numpy arrays for easy handline
    #print(X)
    X = np.array(X, dtype=float).T
    y = np.array(y, dtype = float)
    for k, v in x_control.items(): x_control[k] = np.array(v, dtype=float)
        
    # shuffle the data
    perm = list(range(0,len(y))) # shuffle the data before creating each fold
    shuffle(perm)
    #print(perm)
    df = pd.read_csv(data_files[0])
    df = df.iloc[perm, :]
    X = X[perm]
    y = y[perm]
    for k in x_control.keys():
        x_control[k] = x_control[k][perm]

    # see if we need to subsample the data
    if load_data_size is not None:
        print("Loading only %d examples from the data" % load_data_size)
        X = X[:load_data_size]
        y = y[:load_data_size]
        for k in x_control.keys():
            x_control[k] = x_control[k][:load_data_size]

    return df, X, y, x_control