from grmpy.simulate.simulate import simulate
from grmpy.estimate.estimate import fit
from grmpy.read.read import read
from grmpy.test.random_init import generate_random_dict
import numpy as np
import pandas as pd

generate_random_dict(constr={'DETERMINISTIC':False})



simulate('test.grmpy.yml')

fit('test.grmpy.yml')



def create_data():
    """This function creates a dataframe according to the data used by Cornelissen et. al. 2018"""

    data = simulate('benedikt.yml')

    # Create birthyear and age at examination year variables

    num_year = data.shape[0] / 4
    num_month = data.shape[0] / 48

    aux_year = np.zeros(data.shape[0])
    aux_month = np.zeros(data.shape[0])
    for counter, year in enumerate([1994, 1995, 1996, 1997]):
        aux_year[int(counter * num_year):int((counter +1) * num_year)] = year
        for subcounter, month in enumerate([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]):
            if int((counter + 1) * num_year + (subcounter + 1) * num_month) > 99999:
                end = int(data.shape[0])
            else:
                end = int((counter + 1) * num_year + (subcounter + 1) * num_month)
            print(int(counter * num_year + (subcounter * num_month)))
            aux_month[int(counter * num_year + (subcounter * num_month)):end] = month
    data['birthyear'] = aux_year
    data['birthmonth'] = aux_month
    data['b4aug'] = (aux_month < 8.0)

    data['age_at_examination'] = np.random.randn()

    # Create time dummies
    for year in [1994, 1995, 1996, 1997]:
        data[str(year)] = (data['birthyear'] == year).astype(float)

    # Create moto variables, predicted school readiness

    aux_dict = {
        1: [0.05, 0.56, 0.06],
        2: [0.05, 0.74, 0.06],
        3: [0.15, 0.79, 0.02],
        4: [0.25, 0.87, 0.06],
        5: [0.25, 0.93, 0.02],
        6: [0.15, 0.97, 0.04],
        7: [0.1, 0.98, 0.01]
    }
    predicted_school_readiness = []
    for quant in aux_dict.keys():
        predicted_school_readiness += \
            (aux_dict[quant][2] * np.random.randn(data.shape[0] *
                                                 aux_dict[quant][0]) + aux_dict[quant][1]).tolist()














