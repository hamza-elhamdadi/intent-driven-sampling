
var sample_sizes = {
    apps: {
        blue: 32437,
        random: 32437,
        maxmin: 32437,
        outlier: 21624,
        vas: 32437
    },
    fraud: {
        blue: 32437,
        random: 32437,
        maxmin: 6407,
        outlier: 32437,
        vas: 9611
    },
    mnist: {
        blue: 6407,
        random: 9611,
        maxmin: 6407,
        outlier: 14416,
        vas: 14416
    },
    pollution: {
        blue: 32437,
        random: 14416,
        maxmin: 32437,
        outlier: 21624,
        vas: 32437
    },
    hidden: {
        blue: 14416,
        random: 21624,
        maxmin: 14416,
        outlier: 32437,
        vas: 32437
    },
}

function selectSampleSize(dataset, method){
    return sample_sizes[dataset][method]
}

for(dataset of ['apps', 'fraud', 'mnist', 'pollution', 'hidden']){
    for(method of ['blue', 'random', 'maxmin', 'outlier', 'vas']){
        console.log(dataset, method, selectSampleSize(dataset, method))
    }
    console.log(' ')
}