from pollination_dsl.alias import InputAlias


"""Alias for annual daylight/radiation radiance parameters."""
rad_par_annual_input = [
    InputAlias.str(
        name='radiance_par',
        description='Text for the radiance parameters to be used for ray tracing. '
        '(Default: -ab 2 -ad 5000 -lw 2e-05).',
        default='-ab 2 -ad 5000 -lw 2e-05',
        platform=['grasshopper']
    )
]


"""Alias for daylight factor radiance parameters."""
rad_par_daylight_factor_input = [
    InputAlias.str(
        name='radiance_par',
        description='Text for the radiance parameters to be used for ray tracing. '
        '(Default: -ab 2 -aa 0.1 -ad 2048 -ar 64).',
        default='-ab 2 -aa 0.1 -ad 2048 -ar 64',
        platform=['grasshopper']
    )
]


"""Alias for thresholds of annual daylight."""
daylight_thresholds_input = [
    InputAlias.str(
        name='thresholds',
        description='A string to change the threshold for daylight autonomy (DA) and '
        'useful daylight illuminance (UDI). Valid keys are -t for daylight autonomy '
        'threshold, -lt for the lower threshold for useful daylight illuminance and '
        '-ut for the upper threshold. The order of the keys is not important '
        'and you can include one or all of them. For instance if you only want '
        'to change the upper threshold to 2000 lux you should use -ut 2000 '
        'as the input. (Default: -t 300 -lt 100 -ut 3000).',
        default='-t 300 -lt 100 -ut 3000',
        platform=['grasshopper']
    )
]
