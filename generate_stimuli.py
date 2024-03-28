from sampling.sample import generate_sample
from sampling.vis import visualize_samples, visualize_pollution_order_samples
from sampling.utils import load_data_params
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

"""
    Experiment 1 Demo 1 Stimuli
"""
def demo1_stimuli():
    plt.rcParams['figure.figsize'] = [14,12]

    df = pd.read_csv('data/control/control.csv')

    # Demo 1
    xvar, yvar = 'socialNbFollowers', 'productsSold'
    filepath = 'visualizations/control/{}.png'

    plt.scatter(df[xvar], df[yvar], s=10, color='maroon')
    plt.savefig(filepath.format('orig'), facecolor='white')

    sizes = [200, 500, 750, 1000, 1500, 2000, 2500, 3000]
    sample = df.copy()
    for size in sizes:
        sample = sample.sample(size)
        plt.clf()
        orig = plt.scatter(df[xvar], df[yvar], s=10, color='maroon')
        orig.remove()
        plt.scatter(sample[xvar], sample[yvar], s=10, color='maroon')
        plt.savefig(filepath.format(size), facecolor='white')

    plt.clf()

"""
    Experiment 1 Demo 2 Stimuli
"""
def demo2_stimuli():
    plt.rcParams['figure.figsize'] = [14,12]

    df = pd.read_csv('data/control/control.csv')
    # Demo 2
    xvar, yvar = 'productsListed', 'socialProductsLiked'
    filepath = 'visualizations/control2/{}.png'

    plt.scatter(df[xvar], df[yvar], s=10, color='maroon')
    plt.savefig(filepath.format('orig'), facecolor='white')

    sizes = [1600, 1400, 1200, 1000, 800, 600, 400, 200]
    sample = df[df[xvar] > 19]
    for size in sizes:
        sample = sample.sample(size)
        plt.clf()
        orig = plt.scatter(df[xvar], df[yvar], s=10, color='maroon')
        orig.remove()
        plt.scatter(sample[xvar], sample[yvar], s=10, color='maroon')
        plt.savefig(filepath.format(size), facecolor='white')

    plt.clf()

"""
    Experiment 1 Attention Check Stimulus
"""

def attention_check_stimulus():
    plt.rcParams['figure.figsize'] = [20, 5]

    data = [np.arange(1,10)]
    titles = ['Original', 'Sample A', 'Sample B', 'Sample C']


    data.append(np.array([5]))
    data.append(np.arange(1,10,2))
    data.append(data[0][np.random.choice(9, 8, replace=False)])

    fig, ax = plt.subplots(1, 4)

    for i in range(4):
        ax[i].scatter(data[i], data[i], s=60)
        ax[i].set_xlim([0,10])
        ax[i].set_ylim([0,10])
        ax[i].set_title(titles[i], fontsize=20)
        ax[i].set_xlabel('X', fontsize=18)
        ax[i].set_ylabel('Y', fontsize=18)

    fig.tight_layout()
    plt.savefig('attention_check.png', facecolor='white')

    plt.clf()

"""
    Experiment 1 Stimuli
"""
def experiment1_stimuli():
    sizes = [250, 375, 563, 844, 1266, 1898, 2848, 4271, 6407, 9611, 14416, 21624, 32437]
    methods = ['maxmin', 'random', 'blue', 'outlier', 'vas']
    variables = load_data_params()


    for v in variables:
        for method in methods:
            generate_sample(
                props=v,
                sample_sizes=sizes,
                method=method,
                keepold=False,
                verbose=True
            )

        visualize_samples(
            props=v,
            sample_sizes=sizes,
            methods=methods,
            trim=v['folder']=='apps',
            x_rotate='vertical' if 'pollution' in v['folder'] else None,
            y_lim=[0,5.5] if v['folder'] == 'apps' else None,
            y_ticks=range(1,6) if v['folder'] == 'apps' else None
        )

"""
    Experiment 2 Stimuli
"""
def experiment2_stimuli():
    sizes = [250, 375, 563, 844, 1266, 1898, 2848, 4271, 6407, 9611, 14416, 21624, 32437]
    methods = ['maxmin', 'random', 'blue', 'outlier', 'vas']
    variables = load_data_params()[1:2]

    for v in variables:
        visualize_samples(
            props=v,
            sample_sizes=sizes,
            methods=methods,
            trim=v['folder']=='apps',
            x_rotate='vertical' if 'pollution' in v['folder'] or 'apps' in v['folder'] else None,
            y_lim=[0,5.5] if v['folder'] == 'apps' else None,
            y_ticks=range(1,6) if v['folder'] == 'apps' else None,
            axis_labels=True
        )
    
if __name__ == '__main__':
    sizes = [250, 375, 563, 844, 1266, 1898, 2848, 4271, 6407, 9611, 14416, 21624, 32437]
    methods = ['maxmin', 'random', 'blue', 'outlier', 'vas']
    for method in methods:
        if not os.path.exists(os.path.join('exp2','pollution_order',method)):
            os.mkdir(os.path.join('exp2','pollution_order',method))
    visualize_pollution_order_samples(sample_sizes=sizes, methods=methods)
    experiment2_stimuli()