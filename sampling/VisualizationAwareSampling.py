from sampling.utils import normalize_numeric_columns
import numpy as np

def estimateK(data, sample_ids, new_point, epsilon):
    distances_row = np.sqrt(np.sum(np.square(data[sample_ids] - data[new_point]), axis=1))
    return np.exp( -( distances_row**2 / (2 * epsilon**2) ) )

def expand(data, solution_ids, rsp_values, new_point, epsilon):
    k_values = estimateK(data, solution_ids, new_point, epsilon)

    solution_ids = np.append(solution_ids, new_point)

    rsp_values += k_values
    rsp_values = np.append(rsp_values, np.sum(k_values))
    
    return solution_ids, rsp_values     

def shrink(data, solution_ids, rsp_values, epsilon):
    # Find the index of the max rsp value in rsp_values and the corresponding point in solution_ids. 
    max_index = np.argmax(rsp_values)
    point_to_remove = solution_ids[max_index]

    solution_ids = np.delete(solution_ids, max_index)

    rsp_values = np.delete(rsp_values, max_index)
    rsp_values -= estimateK(data, solution_ids, point_to_remove, epsilon)
    
    return solution_ids, rsp_values  


def VisualizationAwareSample(data, k, repeat=1):
    X = normalize_numeric_columns(data)

    N, d = X.shape
    indices = np.random.permutation(N)
    epsilon = np.sqrt(d)/100
    

    solution_ids, rsp_values = indices[:k], []
    for index in solution_ids:
        rsp_values.append(np.sum(estimateK(X, solution_ids, index, epsilon)))

    for index in indices[k:]: 
        card = len(solution_ids)       
        solution_ids, rsp_values = expand(X, solution_ids, rsp_values, index, epsilon)
        if card >= k:   
            solution_ids, rsp_values = shrink(X, solution_ids, rsp_values, epsilon)

    num_iters, prev_total = 0, 0
    while True:
        indices = np.random.permutation(N)
        for index in indices:
            if index not in solution_ids:
                    solution_ids, rsp_values = expand(X, solution_ids, rsp_values, index, epsilon)
                    solution_ids, rsp_values = shrink(X, solution_ids, rsp_values, epsilon)
                    
        curr_total = np.sum(rsp_values)
        delta = np.square(curr_total - prev_total)
        prev_total = curr_total

        num_iters += 1
        if delta < 1e-4:
            print('num iters:', num_iters)
            return data.iloc[solution_ids]

