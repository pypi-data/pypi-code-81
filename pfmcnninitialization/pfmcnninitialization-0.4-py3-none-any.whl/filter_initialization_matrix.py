import numpy as np
import wget
import pandas as pd
from random import randint, sample
def filter_initialization_matrix(taxonomic_groups='plants',data_local = None,
                                 filters=64,
                                 L_=8,
                                 pattern='ppm_rp25',
                                 background_acgt=[0.25, 0.25, 0.25, 0.25]):
    print('Note that the base order in the return result matrix is ACGT')
    #只有pwm模式，需要background_acgt
    if pattern == 'ppm_rp25':
        print(
            'You will get the PPM_R25 matrix((the value of each position of the PPM matrix is subtracted by 0.25)) with the specified number and length.'
        )
        pfm = get_pfm(taxonomic_groups,data_local )
        ppm = get_ppm(pfm)
        ppm_L = get_ppm_rp25_L(ppm, L_)
        sample_number = [randint(0, len(ppm_L) - 1) for _ in range(filters)]
        ppm_r25_filters = []
        for i in sample_number:
            ppm_r25_filters.append(ppm_L[i])
        print('You will get the numpy array with shape ',
              str(np.array(ppm_r25_filters).shape))
        print(
            "You can use numpy's swaaxes function to make the dimension transformation suitable for initializing your parameters"
        )
        return np.array(ppm_r25_filters)
    elif pattern == 'ppm':
        print(
            'You will get the PPM matrix with the specified number and length.'
        )
        pfm = get_pfm(taxonomic_groups,data_local )
        ppm = get_ppm(pfm)
        ppm_L = get_ppm_L(ppm, L_)
        sample_number = [randint(0, len(ppm_L)-1) for _ in range(filters)]
        ppm_filters = []
        for i in sample_number:
            ppm_filters.append(ppm_L[i])
        print('You will get the numpy array with shape ',
              str(np.array(ppm_filters).shape))
        print(
            "You can use numpy's swaaxes function to make the dimension transformation suitable for initializing your parameters"
        )
        return np.array(ppm_filters)
    elif pattern == 'pwm':
        print(
            'You will get the PWM matrix of the specified length and the specified number calculated with '
            + str(background_acgt) + ' as the background.',
            'To prevent negative infinity, the value of 1e-2 is added to all positions.'
        )
        pfm = get_pfm(taxonomic_groups,data_local )
        ppm = get_ppm(pfm)
        ppm_L = get_ppm_L(ppm, L_)
        pwm = get_pwm(ppm_L, background_acgt)
        sample_number = [randint(0, len(pwm)-1) for _ in range(filters)]
        pwm_filters = []
        for i in sample_number:
            pwm_filters.append(pwm[i])
        print('You will get the numpy array with shape ',
              str(np.array(pwm_filters).shape))
        print(
            "You can use numpy's swaaxes function to make the dimension transformation suitable for initializing your parameters"
        )
        return np.array(pwm_filters)