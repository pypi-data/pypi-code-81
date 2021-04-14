import numpy as np

def merge_data(data, metric):
    merged_outcomes = {}
    for key in data.keys():
        results = data[key]
        if metric == 1:
            merged_outcomes[key] = list(map(np.mean, zip(*results)))
        if metric == 2:
            merged_outcomes[key] = list(map(min, zip(*results)))
        if metric == 3:
            merged_outcomes[key] = list(map(max, zip(*results)))
    return merged_outcomes
