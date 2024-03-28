from sampling.OutlierBiasedDensitySampling import OutlierBiasedDensitySample
from sampling.CoverSetSampling import CoverSetSample
from sampling.BlueNoiseSampling import BlueNoiseSample
from sampling.DiverseSampling import DiverseSample
from sampling.VisualizationAwareSampling import VisualizationAwareSample
from sampling.utils import load_to_df, get_dataset_filepath, get_sample_filepath, get_three_dimensional_data
import numpy as np
import os

def _sample(df, attrib, method, size, prob=None):                                           # function to call the correct sampling method based on "method" parameter
    if method == 'random':                                                                  # if random sampling
        return df.sample(size)                                                              #   return uniform random sample of sample size (size)
    elif method == 'coverset':                                                              # else if coverset
        return CoverSetSample(df, attrib, size)                                             #   return coverset sample of size (size) with categories defined by attribs[0] 
    elif method == 'blue':                                                                  # else if blue noise sampling
        return BlueNoiseSample(df, size, verbose=True)                                      #   return blue noise sample of size (size)
    elif method == 'outlier':                                                               # else if outlier biased density sampling
        return OutlierBiasedDensitySample(df, size, attrib, prob=prob, verbose=True)        #   return outlier biased density sample of size (size)
    elif method == 'maxmin' or method == 'maxsum':                                          # else if maxmin or maxsum
        return DiverseSample(df, size, method)                                              #   return corresponding diverse sample of size (size)
    elif method == 'vas':                                                                   # else if visualization aware sampling
        return VisualizationAwareSample(df, size)                                           #   return visualization aware sample of size(size)
    else:
        return None

def generate_sample(props, sample_sizes, method='random', keepold=False, verbose=False):
    print(props, sample_sizes, method)
    samples = [] 
    probs = []
    sample_sizes = np.sort(sample_sizes)[::-1]

    df = load_to_df(get_dataset_filepath(props), props)
    if verbose:
        print('file read')
    
    maxpath = get_sample_filepath(props, method, sample_sizes[0])
    if method == 'outlier':
        s, p = _sample(df, props['attrib'], method, sample_sizes[0])
        probs.append(p)
    elif keepold and os.path.exists(maxpath):
        s = load_to_df(maxpath, props)
    else:
        s = _sample(df, props['attrib'], method, sample_sizes[0])
    samples.append(s)

    for i, size in enumerate(sample_sizes):
        if method in ['coverset', 'blue']:
            s = _sample(samples[i], props['attrib'], method, size)
        elif method == 'vas':
            s = _sample(df, props['attrib'], method, size)
        elif method == 'outlier':
            s, p = _sample(samples[i], props['attrib'], method, size, probs[i])
            probs.append(p)
        else:
            s = samples[i].head(size).fillna(0)

        samples.append(s)

        sample = np.column_stack(get_three_dimensional_data(s, props))

        outpath = get_sample_filepath(props, method, size)
        np.save(outpath, sample)
        print(outpath)