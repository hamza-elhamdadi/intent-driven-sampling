from sampling.utils import adjust_sample_size, reduce_num, normalize_numeric_columns
from sklearn.neighbors import NearestNeighbors
import scipy.stats as stats
import numpy as np
import pandas as pd
import time

def BlueNoiseSample(df, sampling_rate, use_step=True, max_step=25, return_radius=False, verbose=False):
    blue_noise_fail_rate = 0.1

    n, _ = df.shape
    m = adjust_sample_size(len(df), sampling_rate)
    total_k = int(n / m) + 1

    if use_step and total_k != 1:
        ks = reduce_num(total_k, max_step=max_step, arr=[])
    else:
        ks = np.array([total_k]) + 1

    ks = np.sort(ks)[::-1]

    out = df
    for k_idx, k in enumerate(ks):
        n, _ = out.shape
        mp = m if not use_step or k_idx == len(ks)-1 else int(n/(k-1))
        failure_tolerance = min(5000, (n - mp) * blue_noise_fail_rate)

        if verbose:
            print('current data size:',n)
            print('k:', k)
            
        X = normalize_numeric_columns(out)

        start = time.time()

        knn = NearestNeighbors(n_neighbors=k)   
        knn.fit(X)
        dist, _ = knn.kneighbors(X, return_distance=True)
        radius = np.average(dist[:, -1])
        
        if verbose:
            print('computing k neighbors and radius: t =', time.time()-start)
        
        count, unseen, subset, out_data = 0, None, [], []        

        start = time.time()
        while count < mp:
            this_round = time.time()

            if verbose:
                print('radius:',radius)
            
            fail, unseen = 0, []
            perm = np.random.permutation(unseen or n)

            for i, idx in enumerate(perm):
                if fail > failure_tolerance or count >= mp:
                    unseen += perm[i:].tolist()
                    break
                if len(subset) == 0:
                    success = True
                else:
                    success = np.min(np.sum(np.square(np.array(subset)-X[idx]),axis=1)) >= radius**2

                if success:
                    count += 1
                    subset.append(X[idx])
                    out_data.append(out.iloc[idx])
                else:
                    unseen.append(idx)
                    fail += 1

            radius /= 2

            if verbose:
                print(f'current count {count}, t = {time.time()-this_round}')

        if verbose:
            print('picking points: t =', time.time()-start)
            print()

        out = pd.DataFrame(out_data, columns=df.columns)

        k /= 10

    if return_radius:
        return out, radius*2
    
    return out

def compute_power_spectrum(data):
    npix = data.shape[0]

    f      = np.fft.fftn(data)
    amp    = np.abs(f)**2
    freq   = np.fft.fftfreq(npix) * npix
    freq2d = np.meshgrid(freq, freq)
    nrm    = np.sqrt(freq2d[0]**2 + freq2d[1]**2).flatten()

    bins   = np.arange(0.5, npix//2+1, 1.)
    vals   = 0.5 * (bins[1:] + bins[:-1])
    amp    = amp.flatten()

    Abins,_,_ = stats.binned_statistic(nrm, amp, statistic='mean', bins=bins)
    Abins *= np.pi * (bins[1:]**2 - bins[:-1]**2)
    
    return vals, Abins

def compute_magnitudes(data):
    f      = np.fft.fft2(data)
    fshift = np.fft.fftshift(f)
    mag    = 20*np.log(np.abs(fshift))

    return mag