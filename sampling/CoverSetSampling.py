from sampling.utils import adjust_sample_size
from sampling.testing import test_coverset
import pandas as pd
import numpy as np

def CoverSetSample(df, attrib, sample):                                         # coverset sampling
    sample = adjust_sample_size(len(df),sample)                                 # adjust sample size (if it's between 0 and 1, make it between 0 and n)
    
    cats, total_points = np.unique(df[attrib].to_numpy(), return_counts=True)   # get list and frequency of unique categories
    orders = np.argsort(total_points)                                           # get sorted frequency indices
    cats, total_points = cats[orders], total_points[orders]                     # sort cats and total_points

    if len(cats) > sample:
        raise ValueError('The number of unique labels in the specified attribute is greater than the sample size')

    points_per_cat, slack = divmod(sample, len(cats))                           # compute the initial slack and points per category
    points_per_cat += np.zeros(len(cats), dtype=int)                            # map to vector of length len(cats)

    subset = pd.DataFrame([], columns = list(df.columns))                       # create an empty dataframe with the columns of the original dataset
    
    for i, cat in enumerate(cats):                                              # iterate through each category - O(c) where c <= n
        swap = min(total_points[i] - points_per_cat[i], slack)
        slack -= swap
        points_per_cat[i] += swap
    
        sample_from_cat = df[df[attrib] == cat].head(points_per_cat[i])         # sample the points from this category
        subset = pd.concat([subset, sample_from_cat],axis=0)                    # add these points to the dataframe
    
    test_coverset(subset, sample, points_per_cat, total_points, cats)

    return subset

