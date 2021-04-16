#! /usr/bin/env python

from copy import deepcopy

def lowercase_dict_keys(indict):
    """To make reference file override dictionary creation easier for
    users, allow the input keys to be case insensitive. Take the user
    input dictionary and translate all the keys to be lower case.
    """
    lower1 = {}
    for key1, val1 in indict.items():
        if isinstance(val1, dict):
            lower2 = {}
            for key2, val2 in val1.items():
                if isinstance(val2, dict):
                    lower3 = {}
                    for key3, val3 in val2.items():
                        if isinstance(val3, dict):
                            lower4 = {}
                            for key4, val4 in val3.items():
                                if isinstance(val4, dict):
                                    lower5 = {}
                                    for key5, val5 in val4.items():
                                        if isinstance(val5, dict):
                                            lower6 = {}
                                            for key6, val6 in val5.items():
                                                lower6[key6.lower()] = val6
                                            lower5[key5.lower()] = deepcopy(lower6)
                                        else:
                                            lower5[key5.lower()] = val5
                                    lower4[key4.lower()] = deepcopy(lower5)
                                else:
                                    lower4[key4.lower()] = val4
                            lower3[key3.lower()] = deepcopy(lower4)
                        else:
                            lower3[key3.lower()] = val3
                    lower2[key2.lower()] = deepcopy(lower3)
                else:
                    lower2[key2.lower()] = val2
            lower1[key1.lower()] = deepcopy(lower2)
        else:
            lower1[key1.lower()] = val1
    indict = lower1
    return indict




def lowercase_dict_keys_3(indict):
    """To make reference file override dictionary creation easier for
    users, allow the input keys to be case insensitive. Take the user
    input dictionary and translate all the keys to be lower case.
    """
    lower1 = {}
    #lower2 = {}
    #lower3 = {}
    #lower4 = {}
    #lower5 = {}
    #lower6 = {}
    for key1, val1 in indict.items():
        if isinstance(val1, dict):
            lower2 = {}
            for key2, val2 in val1.items():
                if isinstance(val2, dict):
                    lower3 = {}
                    for key3, val3 in val2.items():
                        lower3[key3.lower()] = val3
                    lower2[key2.lower()] = deepcopy(lower3)
                else:
                    lower2[key2.lower()] = val2
            lower1[key1.lower()] = deepcopy(lower2)
        else:
            lower1[key1.lower()] = val1
    indict = lower1
    return indict





reffile_overrides = {'nircam': {'SUPERBIAS': {'nrcb5': {'RAPID': {'FULL': 'my_reffiles/my_superbias_for_b5.fits',
                                                                  'SUB160': 'my_reffiles/sub160.fits'
                                                                  },
                                                        'shaLLOW4': 'my_reffiles/sb_shallow.fits'
                                                        },
                                              'nrcb4': 'my_reffiles/my_superbias_for_b4.fits'
                                              },
                                'linearity': {'NRCB5': 'my_reffiles/my_linearity_for_b5.fits',
                                              'nrcb4': 'my_reffiles/my_linearity_for_b4.fits'}
                                },
                     'niriss': {'distortion': {'NIs': 'my_dist.fits'}
                                }
                    }


"""
reffile_overrides = {'nircam': {'SUPERBIAS': {'nrcb5': {'bright1': 'my_reffiles/my_superbias_for_b5.fits',
                                                        'shallow4': 'my_reffiles/my_superbias_for_b5.fits'
                                                        },
                                              'nrcb4': {'shallow2': 'my_reffiles/my_superbias_for_b4.fits'}
                                              },
                                'linearity': {'nrcb5': 'my_reffiles/my_linearity_for_b5.fits',
                                              'nrcb4': 'my_reffiles/my_linearity_for_b4.fits'},
                                'saturation': {'nrcb5': 'my_reffiles/my_saturation_for_b5.fits',
                                               'nrcb4': 'my_reffiles/my_saturation_for_b4.fits'},
                                'gain': {'nrcb5': 'my_reffiles/my_gain_for_b5.fits',
                                         'nrcb4': 'my_reffiles/my_gain_for_b4.fits'},
                                'distortion': {'nrcb5': {'f322w2': {'NRC_IMAGE': 'my_reffiles/my_distortion_for_b5.asdf'}},
                                               'nrcb4': {'f150w': {'NRC_IMAGE': 'my_reffiles/my_distortion_for_b4.asdf'}}},
                                'area': {'nrcb5': {'f322w2': {'clear': {'nrc_image': 'my_reffiles/my_pam_for_b5.fits'}}},
                                         'nrcb4': {'f150w': {'clear': {'nrc_image': 'my_reffiles/my_pam_for_b4.fits'}}}},
                                'transmission': {'nrcb5': {'f322w2': {'clear': 'my_reffiles/my_transmission_for_b5.fits'},
                                                           'f444w': {'clear': 'my_reffiles/my_transmission_for_b5.fits'},
                                                           'f335m': {'clear': 'my_reffiles/my_transmission_for_b5.fits'},
                                                           'f300m': {'clear': 'my_reffiles/my_transmission_for_b5.fits'}},
                                                     'nrcb1': {'f150w': {'clear': 'my_reffiles/my_transmission_for_b1.fits'},
                                                               'f070w': {'clear': 'my_reffiles/my_transmission_for_b1.fits'},
                                                               'f150w2': {'clear': 'my_reffiles/my_transmission_for_b1.fits'},
                                                               'f187n': {'clear': 'my_reffiles/my_transmission_for_b1.fits'}},
                                                     'nrcb2': {'f150w': {'clear': 'my_reffiles/my_transmission_for_b2.fits'},
                                                               'f070w': {'clear': 'my_reffiles/my_transmission_for_b2.fits'},
                                                               'f150w2': {'clear': 'my_reffiles/my_transmission_for_b2.fits'},
                                                               'f187n': {'clear': 'my_reffiles/my_transmission_for_b2.fits'}},
                                                     'nrcb3': {'f150w': {'clear': 'my_reffiles/my_transmission_for_b3.fits'},
                                                               'f070w': {'clear': 'my_reffiles/my_transmission_for_b3.fits'},
                                                               'f150w2': {'clear': 'my_reffiles/my_transmission_for_b3.fits'},
                                                               'f187n': {'clear': 'my_reffiles/my_transmission_for_b3.fits'}},
                                                     'nrcb4': {'f150w': {'clear': 'my_reffiles/my_transmission_for_b4.fits'},
                                                               'f070w': {'clear': 'my_reffiles/my_transmission_for_b4.fits'},
                                                               'f150w2': {'clear': 'my_reffiles/my_transmission_for_b4.fits'},
                                                               'f187n': {'clear': 'my_reffiles/my_transmission_for_b4.fits'}},
                                                    },
                                    'badpixmask': {'nrcb5': 'my_reffiles/my_bpm_for_b5.fits',
                                                   'nrcb4': 'my_reffiles/my_bpm_for_b4.fits'},
                                    'pixelflat': {'nrcb5': {'f322w2': {'clear': 'my_reffiles/my_flatfield_for_b5.fits'}}}
                                    },
                         'niriss': {'superbias': {'nisrapid': 'my_niriss_supebias.fits'},
                                    'linearity': 'my_niriss_linearity,fits',
                                    'saturation': 'my_niriss_saturation.fits',
                                    'gain': 'my_niriss_gain.fits',
                                    'distortion': {'F115W': {'nis_image': 'my_niriss_disotrtion.asdf'}},
                                    'area': {'clear': {'f115w': {'nis_image': 'my_niriss_area.fits'}}},
                                    'transmission': {'clear': {'f115w': 'my_niriss_transmission.fits'},
                                                     'gr150c': {'f115w': 'my_niriss_gr_transmission.fits'}
                                                     },
                                    'badpixmask': 'my_niriss_badpixmask.fits',
                                    'pixelflat': {'clear': {'f115w': 'my_niriss_flatfield.fits'}}
                                    }
                         }
"""

for key in reffile_overrides:
    print(key, reffile_overrides[key])

print('\n\n')
lower = lowercase_dict_keys(reffile_overrides)
for key in lower:
    print(key, lower[key])

