import numpy as np


def merge_data(data, outcomes, repetitions, metric):
    for key in outcomes.keys():
        scenario_avgs = []
        for scenario in range(len(outcomes[key])):
            results = []
            for replication in range(repetitions):
                if metric == 1:
                    results.append(np.mean(outcomes[key][scenario][replication]))
                if metric == 2:
                    results.append(min(outcomes[key][scenario][replication]))
                if metric == 3:
                    results.append(max(outcomes[key][scenario][replication]))
                if metric == 4:
                    results.append(outcomes[key][scenario][replication][-1])
            scenario_avgs.append(np.mean(results))

        data[key] = scenario_avgs
    return data
