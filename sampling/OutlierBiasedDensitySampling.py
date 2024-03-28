from sampling.utils import adjust_sample_size, normalize_numeric_columns
from sklearn.neighbors import NearestNeighbors
import numpy as np
import time

def OutlierBiasedDensitySample(df, sampling_rate, label, alpha=1, beta=1, prob=None, verbose=False):
    m = adjust_sample_size(len(df), sampling_rate)
    if prob is None:
        k = 50

        if verbose:
            print('normalizing data')
            start = time.time()

        X = normalize_numeric_columns(df)

        if verbose:
            print('data normalized, t =', time.time()-start)
        
        n, _ = X.shape
        if k + 1 > n:
            k = int((n - 1) / 2)

        category = df[label].to_numpy()

        if verbose:
            print('running knn with 52 neighbors')
            start = time.time()

        knn = NearestNeighbors(n_neighbors=k+2)   
        knn.fit(X)
        dist, neighbor = knn.kneighbors(X, return_distance=True)

        if verbose:
            print('knn done, t =', time.time()-start)
            print('computing outlier score')
            start = time.time()

        neighbor_labels = category[neighbor]
        outlier_score = [sum(neighbor_labels[i] != category[i]) for i in range(n)]
        outlier_score = np.array(outlier_score) / k

        if verbose:
            print(outlier_score)
            print('outlier score computed, t =', time.time()-start)
            print('getting normalized radius of kth neighbor')
            start = time.time()

        radius_of_k_neighbor = dist[:,-1]
        minD = np.min(radius_of_k_neighbor)
        Z = max(1, np.max(radius_of_k_neighbor) - minD)
        radius_of_k_neighbor = ((radius_of_k_neighbor - minD) / Z) / 2 + 0.5

        if verbose:
            print(radius_of_k_neighbor)
            print('normalized radius of kth neighbor computed, t =', time.time()-start)
            print('setting probability for each point and selecting points according to the distribution')

        prob = alpha * radius_of_k_neighbor + beta * outlier_score
    
    start = time.time()
    n, _ = df.shape
    prob = prob / prob.sum()
    selected_indexes = np.random.choice(n, m, replace=False, p=prob)

    if verbose:
        print(prob)
        print('points chosen, t =', time.time()-start)
    
    return df.iloc[selected_indexes], prob[selected_indexes]
