from pollination_dsl.alias import InputAlias


"""Alias for simulation run periods."""
run_period_input = [
    InputAlias.str(
        name='run_period',
        description='An AnalysisPeriod to set the start and end dates of the '
        'simulation. If None, the simulation will be annual.',
        default='',
        platform=['grasshopper']
    )
]
