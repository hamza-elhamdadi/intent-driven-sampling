from sampling.utils import load_to_df, load_data_params, get_dataset_filepath, get_sample_filepath
import matplotlib.pyplot as plt
import os
import numpy as np, pandas as pd

def trim_num(num):
    num, k, m, b = [int(int(num) // 1e3**i) for i in range(4)]
    return f'{b}B' if b >= 1 else f'{m}M' if m >= 1 else f'{k}K' if k >= 1 else f'{num}'

def vis_helper(ax,x,y,plotType, a=None):
    if plotType == 'bar':
        return ax.bar(x,y,color='maroon',width=0.4,align='center')
    else:
        return ax.scatter(x,y,color='maroon',s=10,alpha=a)

def visualize_samples(props, sample_sizes, methods, trim=False, x_rotate=None, y_lim=None, y_ticks=None, axis_labels=False):
    plt.rcParams['figure.figsize'] = [14,12]
    x, y = props['x'], props['y']
    plotType = props['plotType']
    folder = props['folder']

    df_old = load_to_df(get_dataset_filepath(props), props)
    df_old = df_old.drop(df_old.columns.difference([x,y]), axis=1)
    df = df_old.groupby(x).mean().reset_index() if plotType == 'bar' else df_old

    df_min, df_max = df.min(), df.max()

    if axis_labels and folder == 'fraud':
        df['city_pop'] = df['city_pop'] / 1e6

    if axis_labels and (folder == 'mnist' or folder == 'hidden'):
        df[x] = (df[x] + np.abs(df[x].min())) / (df[x].max() - df[x].min()) * 3.0
        df[y] = (df[y] + np.abs(df[y].min())) / (df[y].max() - df[y].min()) * 30000

    if trim:
        df[x] = df[x].apply(trim_num)

    fig, ax = plt.subplots()
    vis_helper(ax, df[x], df[y], plotType)

    if x_rotate:
        ax.set_xticks(df[x], df[x], rotation=x_rotate, fontsize=16)

    if y_lim:
        ax.set_ylim(y_lim)
    
    if y_ticks:
        ax.set_yticks(y_ticks, labels=y_ticks)
    
    if axis_labels:
        ax.set_xlabel(props['xlabel'], size=20)
        ax.set_ylabel(props['ylabel'], size=20)
        
    outpath = os.path.join(f'exp{1+axis_labels}',folder,'orig.png')
    fig.tight_layout()
    fig.savefig(outpath, facecolor='white')
    # plt.clf()
    print(outpath)

    for method in methods:
        for size in sample_sizes:
            filepath = get_sample_filepath(props, method, size)
            if not os.path.exists(filepath):
                print(f'Warning: File Not Found: {filepath}')
            sample = load_to_df(filepath, props)
            sample = sample.drop(sample.columns.difference([x,y]), axis=1)
            sample[y] = sample[y].apply(float)

            if axis_labels and folder == 'fraud':
                sample[x] = sample[x] / 1e6

            if axis_labels and (folder == 'mnist' or folder == 'hidden'):
                sample.loc[len(sample)] = df_min
                sample.loc[len(sample)] = df_max
                sample[x] = (sample[x] + np.abs(sample[x].min())) / (sample[x].max() - sample[x].min()) * 3.0
                sample[y] = (sample[y] + np.abs(sample[y].min())) / (sample[y].max() - sample[y].min()) * 30000
                sample = sample.iloc[:-2]

            if plotType == 'bar':
                sample = sample.groupby(x).mean().reset_index()

            if trim:
                sample[x] = sample[x].apply(trim_num)
            
            fig, ax = plt.subplots()

            tick_data = vis_helper(ax, df[x], df[y], plotType, None)
            tick_data.remove()
            vis_helper(ax, sample[x], sample[y], plotType, None)
            
            if x_rotate:
                ax.set_xticks(df[x], df[x], rotation=x_rotate, fontsize=16)
            else:
                ax.tick_params(axis='x', labelsize=18)
            
            if y_lim:
                ax.set_ylim(y_lim)

            if y_ticks:
                ax.set_yticks(y_ticks, labels=y_ticks, fontsize=18)
            else:
                ax.tick_params(axis='y', labelsize=18)

            if axis_labels:
                ax.set_xlabel(props['xlabel'], size=20)
                ax.set_ylabel(props['ylabel'], size=20)
            
            fig.tight_layout()
            outpath = os.path.join(f'exp{1+axis_labels}',folder,method,f'{size}.png')
            fig.savefig(outpath, facecolor='white')
            # plt.clf()
            print(outpath)

def visualize_pollution_order_samples(sample_sizes, methods):
    plt.rcParams['figure.figsize'] = [14,12]
    x, y = 'State', 'CO AQI'

    df = pd.read_csv('data/pollution/pollution.csv')
    df = df.drop(df.columns.difference([x,y]), axis=1)
    df = df[(df[x] == 'District Of Columbia') | (df[x] == 'Arizona') | (df[x] == 'Colorado') | (df[x] == 'South Dakota') | (df[x] == 'North Dakota') | (df[x] == 'Wyoming')]
    df = df.groupby(x).mean().reset_index()

    fig, ax = plt.subplots()

    tick_data = vis_helper(ax, df[x], df[y], 'bar', None)
    tick_data.remove()
    vis_helper(ax, df[x], df[y], 'bar', None)
    
    ax.set_xticks(df[x], df[x], rotation='vertical', fontsize=16)
    ax.tick_params(axis='y', labelsize=18)
    ax.set_xlabel('Location', size=20)
    ax.set_ylabel('Average Carbon Monoxide Air Quality Index', size=20)
    
    fig.tight_layout()
    outpath = os.path.join('exp2','pollution_order','orig.png')
    fig.savefig(outpath, facecolor='white')
    print(outpath)

    for method in methods:
        for size in sample_sizes:
            filepath = os.path.join('data', 'pollution', '_'.join(('pollution', method, str(size))) + '.npy')
            if not os.path.exists(filepath):
                print(f'Warning: File Not Found: {filepath}')
            sample = load_to_df(filepath, load_data_params()[1])
            sample = sample.drop(sample.columns.difference([x,y]), axis=1)
            sample = sample[(sample[x] == 'District Of Columbia') | (sample[x] == 'Arizona') | (sample[x] == 'Colorado') | (sample[x] == 'South Dakota') | (sample[x] == 'North Dakota') | (sample[x] == 'Wyoming')]
            sample[y] = sample[y].apply(float)
            sample = sample.groupby(x).mean().reset_index()
            
            fig, ax = plt.subplots()

            tick_data = vis_helper(ax, df[x], df[y], 'bar', None)
            tick_data.remove()
            vis_helper(ax, sample[x], sample[y], 'bar', None)
            
            ax.set_xticks(df[x], df[x], rotation='vertical', fontsize=16)
            ax.tick_params(axis='y', labelsize=18)
            ax.set_xlabel('Location', size=20)
            ax.set_ylabel('Average Carbon Monoxide Air Quality Index', size=20)
            
            fig.tight_layout()
            outpath = os.path.join('exp2','pollution_order',method,f'{size}.png')
            fig.savefig(outpath, facecolor='white')
            print(outpath)