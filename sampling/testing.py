from sampling.DiverseSampling import DiverseSample
from pandas.testing import assert_frame_equal
import pandas as pd
import numpy as np

def verify_sample_size(S, size):
    try:
        assert len(S) == size
    except:
        print('Sample does not have correct size')

def test_diverse(D, S, size, start, type='maxmin', validate=False):
    if not isinstance(D, pd.DataFrame):
        D = pd.DataFrame(D)
    if not isinstance(S, pd.DataFrame):
        S = pd.DataFrame(S)

    sample = DiverseSample(D, size, type, start, validate)

    try:
        assert_frame_equal(sample, S, check_names=False)
    except:
        print('output of diverse sampling not correct')
        print(sample.compare(S))

def test_coverset(S, size, points_per_cat, total_points, cats):
    try:
        assert (points_per_cat<=total_points).all()                             # check that we didn't take more points from any category than that category had in total
    except:
        print('something went wrong')
        print('points_per_cat:', points_per_cat)
        print('total_points', total_points)

    try:
        assert np.sum(points_per_cat) == size                                   # check that we intended to take (sample) number of points
    except:
        print('something went wrong')
        print(f'np.sum(points_per_cat) = {np.sum(points_per_cat)} != {size}')
        print('points_per_cat:', points_per_cat)
        print('total_points:', total_points)

    try:
        b = size//len(cats)
        x = points_per_cat>=b
        y = total_points<b
        assert (x + y).all()                                                    # check that for each category, we either took b points or more, or that category had fewer than b points available
    except: 
        print('something went wrong')
        print(x)
        print(y)
        print(x+y)

    verify_sample_size(S, size)                                                 # check that we actually took (sample) number of points

def test_blue_noise(S, size, radius):
    verify_sample_size(S, size)

    for i in range(S.shape[0]):
        try:
            dist = np.sqrt(np.sum(np.square(S-S[i]),axis=1))
            assert (dist >= radius).all()
        except:
            idx = np.argmax(dist >= radius)
            print(f'd(S[{i}],S[{idx}]) = {dist[idx]} < {radius}')
            break

def collagify_mnist(img):
    coll_shape = (240,240,3) if img.shape[-1] == 3 else (240,240)
    collage = np.zeros(coll_shape)
    collage[:80,0:80]       = img[120:200,560:640]
    collage[:80,80:160]     = img[200:280,420:500]
    collage[:80,160:240]    = img[340:420,440:520]

    collage[80:160,0:80]    = img[450:530,270:350]
    collage[80:160,80:160]  = img[420:500,640:720]
    collage[80:160,160:240] = img[520:600,400:480]

    collage[160:,0:80]      = img[720:800,300:380]
    collage[160:,80:160]    = img[740:820,520:600]
    collage[160:,160:240]   = img[600:680,700:780]

    return collage