import pandas as pd
import numpy as np

def create_dict(l): #create a dictionary for elements in l
    idx = [i for i in range(0, len(l))]
    zobj = zip(l, idx)
    hashmap = dict(zobj)
    return hashmap
    

    
def sort_data(df, col): #sort datapoints according to col value
    return df.sort_values(by=col, ascending=False)

def cover_sample(df, attrib, sample=100): #coverage based diversity and fairness (Online Set Selection with Fairness and Diversity Constraints)
    
    cat = len(df[attrib].unique())
    cat_prop = df.groupby([attrib]).size()
    cat_count = np.zeros(cat)
    hashmap = create_dict(df[attrib].unique())
    flor = math.floor(sample/cat)
    cel = math.ceil(sample/cat)
    slack = sample - (cat * flor)
    subset = df[0:0]
    count = 0
    idx = 0
    
    while(count < sample):
        
        #print(df.shape, idx)
        nxt = df.iloc[idx, :]
        c = hashmap.get(nxt[attrib])
        
        if(cat_count[c] < flor):
            subset = subset.append(nxt)
            count += 1
            cat_count[c] += 1
        elif(slack > 0): #cat_count[c] < cel and slack > 0 --> when there are more items per category
            subset = subset.append(nxt)
            count += 1
            cat_count[c] += 1
            slack -= 1
        idx += 1
        
    return subset
        
    
    
def div_maxmin(df, sample=100): #maxmin diversity based sampling
    
    df = df.sample(frac=1)
    allpair_dist = allpair_distance(df) #compute the distance using function defined by you
    subset = df[0:0]
    subset = subset.append(df.iloc[0, :])
    
    candidate = np.ones(df.shape[0])
    candidate[0] = 0
    dist = allpair_dist[0, :]
    print(dist.shape)
    
        
    while(subset.shape[0] < sample):
        idx = np.argmax(dist)
        subset = subset.append(df.iloc[idx, :])
        candidate[idx] = 0
        dist = np.minimum(dist, allpair_dist[idx, :]) * candidate
        
    return subset

def div_maxsum(df, sample=100): #maxsum diversity based sampling
    
    df = df.sample(frac=1)
    allpair_dist = allpair_distance(df)
    subset = df[0:0]
    subset = subset.append(df.iloc[0, :])
    
    candidate = np.ones(df.shape[0])
    candidate[0] = 0
    dist = allpair_dist[0, :]
    
    while(subset.shape[0] < sample):
        idx = np.argmax(dist)
        subset = subset.append(df.iloc[idx, :])
        candidate[idx] = 0
        dist = (dist + allpair_dist[idx, :]) * candidate
        
    return subset

def num_neighbr(dist, radius):
     
    dist[dist < radius] = 1
    dist[dist >= radius] = 0
    
    return np.sum(dist, axis=1)
    
def div_disc(df, radius, temp, sample=100): #DisC diversity based sampling
    
    allpair_dist = allpair_distance(df)
    allpair_dist = temp
    subset = df[0:0]
    color = np.zeros(df.shape[0])
    neighbor = num_neighbr(allpair_dist.copy(), radius)
    
    while(0 in color):
        idx = np.argmax(neighbor)
        subset = subset.append(df.iloc[idx, :])
        neighbor[idx] = -1
        color[idx] = -1
        color[allpair_dist[idx, :] < radius] = -1
        neighbor[allpair_dist[idx, :] < radius] = -1
        d = dict(zip(*np.unique(color, return_counts=True)))
        
    print(subset.shape)
        
    return subset        
        
        
    