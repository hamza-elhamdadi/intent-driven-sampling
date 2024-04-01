def create_dict(l): #create a dictionary for elements in l
    idx = [i for i in range(0, len(l))]
    zobj = zip(l, idx)
    hashmap = dict(zobj)
    return hashmap


def maxmin_fair(df, attrib, dist, flor=None, cel=None, sample=100): 
    
    cat_count = dict.fromkeys(flor.keys(), 0)
    slack = sample - (sum(flor.values()))    
    subset = df[0:0]
    count = 1
    idx = 0
    
    allpair_dist = dist
    candidate = np.ones(df.shape[0])
    first = np.random.choice(np.arange(0, df.shape[0]), 1)
    dist = allpair_dist[first, :]
    candidate[first] = 0
    subset = subset.append(df.iloc[first, :])
    
    while(count < sample):
        
        #print(df.shape, idx)
        idx = np.argmax(dist)
        candidate[idx] = 0
        dist = np.minimum(dist, allpair_dist[idx, :]) * candidate
        nxt = df.iloc[idx, :]
        c = nxt[attrib]
        
        if(cat_count[c] < flor[c]):
            subset = subset.append(nxt)
            count += 1
            cat_count[c] += 1
        elif(slack > 0): 
            subset = subset.append(nxt)
            count += 1
            cat_count[c] += 1
            slack -= 1    
    return subset

def maxsum_fair(df, attrib, dist, flor=None, cel=None, sample=100): 
    
    cat_count = dict.fromkeys(flor.keys(), 0)
    slack = sample - (sum(flor.values()))    
    subset = df[0:0]
    count = 1
    idx = 0
    
    allpair_dist = dist
    candidate = np.ones(df.shape[0])
    first = np.random.choice(np.arange(0, df.shape[0]), 1)
    dist = allpair_dist[first, :]
    candidate[first] = 0
    subset = subset.append(df.iloc[first, :])
    
    while(count < sample):
        
        idx = np.argmax(dist)
        candidate[idx] = 0
        dist = (dist + allpair_dist[idx, :]) * candidate
        nxt = df.iloc[idx, :]
        c = nxt[attrib]
        
        if(cat_count[c] < flor[c]):
            subset = subset.append(nxt)
            count += 1
            cat_count[c] += 1
        elif(slack > 0): 
            subset = subset.append(nxt)
            count += 1
            cat_count[c] += 1
            slack -= 1    
    return subset
