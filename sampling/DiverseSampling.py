from sampling.utils import adjust_sample_size, distance_row, normalize_numeric_columns
from random import randint as rnd
import pandas as pd
import numpy as np

def DiverseSample(df, sample=1, type='maxmin', start=None, validate=False):                                        # maxmin or maxsum diversity based sampling
    data = normalize_numeric_columns(df)                                                                                   # convert numeric dataframe to 2d numpy array
    points = pd.DataFrame(columns=df.columns)                                                                       # output = new empty dataframe with same columns as input dataframe (including non-numeric)

    starting_index = start if start != None else rnd(0,len(data)-1)                                                 # start the algorithm at a random point in the data if a starting index wasn't passed
    
    if validate:                                                                                                    
        print('first point sampled:',starting_index,data[starting_index])

    points.loc[len(points)] = df.iloc[starting_index].tolist()                                                      # add the starting point to the output dataframe 
    dist = distance_row(data, starting_index)                                                                       # compute distance from starting point to all other points

    if validate:
        print(f'distances from {data[starting_index]}',dist)
        print(dist)
    
    candidate = np.ones(len(data))                                                                                  # all points are possible candidates initally
    candidate[starting_index] = 0                                                                                   # except we already picked the point at the starting index, so remove that candidate
    sample = adjust_sample_size(len(data),sample)                                                                   # adjust sample if between 0 and 1 to make it between 0 and n
    while(len(points) < sample):                                                                                    # keep adding points until we have the desired sample size
        if len(points) % 100 == 0:                                                                                  
            print(len(points))
        idx = np.argmax(dist)                                                                                       #   pick the point at furthest distance from all other points picked so far
        if validate:
            print('next point sampled:',idx,data[idx])
        points.loc[len(points)] = df.iloc[idx].tolist()                                                             #   add the point to the output dataframe
        candidate[idx] = 0                                                                                          #   remove the point from the list of candidates
        if validate:
            print(f'distances from {data[idx]}',distance_row(data,idx))
        dist = np.minimum(dist, distance_row(data,idx)) if type=='maxmin' else (dist + distance_row(data,idx))      #   adjust the distance vector, pick minimum if maxmin, or sum new distance and old distance vector if maxsum 
        if validate:
            print(f"distances after {'minimizing' if type == 'maxmin' else 'summing'}",dist)
            print()
        dist *= candidate                                                                                           #   multiply by candidates to make all non-candidates zero in the distance vector

    return points                                                                                                   #   return the output dataframe 

