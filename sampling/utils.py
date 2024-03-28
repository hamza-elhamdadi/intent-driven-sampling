import numpy as np
import pandas as pd
import json
import os

def reduce_num(num, factor=10, max_step=200, arr=[]):
    if num < max_step:
        arr.append(int(num)+1)
        return arr
    next_num = num/factor
    arr.append(factor+1)
    return reduce_num(next_num, factor, max_step, arr)


# function to adjust the sample size to between 
# if sample size is negative, throw an error
# else return sample size * population if m between 0 and 1 otherwise return sample size cast as an integer
def adjust_sample_size(N, m):
    if m < 0:
        raise ValueError('sample size must be positive')
    else:
        return int(m) if m >= 1 else round(N*m)
    

# compute the distance from a single point in a dataset to all other points in the dataset
# return vectorized Euclidean distance
def distance_row(data, idx):                                    
    return np.sqrt(np.sum(np.square(data-data[idx]),axis=1))    



def normalize_numeric_columns(df, type='numpy'):
    X = df.select_dtypes(include=np.number).fillna(0)
    Z = X.max()-X.min()
    X = (X-X.min())/(Z+Z.eq(0))

    X = X.drop('labels', axis=1, errors='ignore')
    X = X.drop('category', axis=1, errors='ignore')

    return X.to_numpy() if type == 'numpy' else X
    

def load_to_df(filepath, props):                                                    # load a file with extensions .csv, .npz, or .npy to a pandas dataframe
    if filepath.endswith('.csv'):                                                   # if file is csv
        return pd.read_csv(filepath)                                                #   return pandas dataframe from the csv file
    
    isnpz = filepath.endswith('.npz')                                               # check if file ends with .npz
    npz = np.load(filepath,allow_pickle=True)                                       # load the file into numpy array
    if not isnpz and npz.shape[0] == 1:                                             # if file is npy and shape is (1,n,m)
        npz = npz[0]                                                                #   reshape to (n,m)

    df_obj = {                                                                      # create a dictionary
        props['x']:      npz['positions'][:,0] if isnpz else npz[:,0],              # with x key containing the x coordinates in the np(y/z) file
        props['y']:      npz['positions'][:,1] if isnpz else npz[:,1],              # with y key containing the y coordinates in the np(y/z) file
        props['attrib']: npz['labels'] if isnpz else npz[:,2]                       # and with labels either zeros (if npy) or the labels from the npz file
    }
    
    return pd.DataFrame.from_dict(df_obj)                                           # return a pandas dataframe created from the dictionary


def load_data_params():
    with open('sampling/data_params.json') as file:
        variables = json.load(file)
    
    return variables

def get_dataset_filepath(props):
    return os.path.join('data', props['folder'], props['dataset'] + props['filetype'])

def get_sample_filepath(props, method, size):
    return os.path.join('data', props['folder'], '_'.join((props['dataset'], method, str(size))) + '.npy')

def get_three_dimensional_data(data, props):
    return (data[props['x']].to_numpy(), data[props['y']].to_numpy(), data[props['attrib']].to_numpy())

# # NOTE: This function only applies to the datasets we use in our study
# # Please create your own utility sorting function for the datasets you intend to use
# def sort_df_by_utility(data):
#     df = data.copy()
#     df_norm = normalize_numeric_columns(df, type='pd')
#     for col in df_norm.columns:
#         df[col] = df_norm[col]

#     # MNIST dataset
#     if 'labels' in df.columns:          
#         cluster_centers = []
#         for cluster in df['labels'].unique():
#             cluster_df = df[df['labels'] == cluster]
#             cluster_centers.append([cluster_df['x'].mean(), cluster_df['y'].mean()])
#         cluster_centers = np.array(cluster_centers)
#         data['utility'] = df.apply(lambda p: -np.min(np.sqrt(np.sum(np.square(cluster_centers-np.array([p['x'], p['y']])), axis=1))), axis=1)
#     # apps and games dataset
#     elif 'minInstalls' in df.columns:   
#         data['utility'] = df.apply(lambda p: np.sum([-p['price'],p['ratings'],p['score'],p['releasedYear']]), axis=1)
#     # fraud dataset
#     elif 'adjusted_pop' in df.columns:  
#         data['utility'] = df.apply(lambda p: np.sum([p['adjusted_pop'],p['adjusted_amt']]), axis=1)
#     # hidden correlation dataset
#     elif 'category' in df.columns:   
#         center = np.array([0.5, 0.5])
#         data['utility'] = df.apply(lambda p: -np.sqrt(np.sum(np.square(center-np.array([p['x'], p['y']])))), axis=1)
#     # pollution dataset
#     elif 'State' in df.columns:  
#         center = np.array([df['NO2 Mean'].mean(), df['O3 Mean'].mean(), df['SO2 Mean'].mean(), df['CO Mean'].mean()])
#         data['utility'] = df.apply(lambda p: -np.sqrt(np.sum(np.square(center-np.array([p['NO2 Mean'], p['O3 Mean'], p['SO2 Mean'], p['CO Mean']])))), axis=1)       
#     else:                               
#         raise ValueError('Dataset is not supported')

#     data = data.sort_values('utility', ascending=False).reset_index(drop=True)
#     data = data.drop('utility', axis=1)

#     return data