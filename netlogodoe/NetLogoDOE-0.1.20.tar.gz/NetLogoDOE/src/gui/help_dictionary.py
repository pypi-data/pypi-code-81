help_text = {
    # Index screen
    'experimental_runs': 'Design an experiment that runs the model with different parameter configurations by specifying '
                         'parameter bounds.\n\n'
                         'The results can be visualised with parallel coordinates, scatter plots and heatmaps.\n\n'
                         'Usage: To determine the effect the model parameters have on the output of the model, '
                         'where the output is defined by NetLogo reporters.',
    'standard_runs': 'Design an experiment that runs the model repeatedly with the same specified parameter values.\n\n'
                     'The results can be visualised with timeseries, histograms, boxplots, violinplots and distribution'
                     ' plots.\n\n'
                     'Usage: To determine the variance of the output for repeated runs of a certain parameter '
                     'configuration, where the output is defined by NetLogo reporters.',
    'import_results': 'Import the saved results of previously run model configurations. Allows access to all the '
                      'visualisations without having to run the model itself.',

    # Import screen
    'import_experiment': 'Import a valid .txt file with saved results from experimental runs.',
    'import_standard': 'Import a valid .txt file with saved results from standard runs.',
    'import_behaviorspace': 'Import a valid .txt file with saved results from the NetLogo BehaviorSpace.',

    # Experiment/Standard screen
    'run_ticks': 'Specify the maximum number of ticks that the simulation can run. If this number is reached, the '
                 'simulation will be stopped.',
    'run_reporters': 'Specify the NetLogo reporters that will be recorded during the simulation.\n'
                     'Every line should only have a single reporter and all of them need to be valid NetLogo '
                     'reporters. Reporters can not be split between lines.\n\n'
                     'Examples:\n'
                     'count sheep\n'
                     'count patches with [pcolor = green]',
    'run_setup': 'Specify the setup commands that will be executed before the simulation starts.\n'
                 'Every line should only have a single command and all of them need to be valid NetLogo commands.',
    'run_processes': 'Specify the number of processes that will execute the simulations in parallel. More processes '
                     'help speed up the overall run time, but will also use more computing power.\n\n'
                     'IMPORTANT: Setting this number too high will bottleneck your computer and could result in a '
                     'slower run time. Make sure to keep an eye on the utilization of your PC in e.g. Task Manager.',
    'save_config': 'Save the experiment in a .txt file somewhere on your PC. This will allow you to import this '
                   'experiment another time so you don\'t need to fill out everything manually again.',

    # Experiment screen
    'experiment_variables': 'Specify the bounds within which the parameter configurations will be generated. Every '
                            'line should only have a single parameter with its lower and upper bound.\n\n'
                            'Examples:\n'
                            'sheep-reproduce 4 6\n'
                            'wolf-reproduce 5 7',
    'experiment_sampling': 'Specify the sampling method that will be used to generate parameter configurations. The '
                           'default is Latin hypercube sampling.\n\n'
                           'Monte Carlo: The parameter values are sampled completely random and independently within '
                           'the parameter bounds\n'
                           'Latin Hypercube: The parameter values are sampled near-random, but depended on each other '
                           'to obtain a good spread.\n'
                           'Full factorial: Every possible configuration between the parameter bounds will be sampled.'
                           ' This method ignores the input for the number of scenarios.\n'
                           'Saltelli: The parameter values are sampled using Saltelli\'s sampling scheme. The number '
                           'of scenarios here needs to adhere to specific conditions, so it may not be the exact '
                           'number that was specified.\n'
                           'Sobol: The parameter values are sampled using Sobol\'s sampling scheme.\n',
    'experiment_scenarios': 'Specify the number of scenarios that will be run for this configuration. Every scenario '
                            'consists of a different set of parameter values that fall within the bounds specified '
                            'above. These parameter values are generated with the selected sampling method.',
    'experiment_repetitions': 'Specify the number of repetitions that will be run for each scenario.',

    # Standard screen
    'standard_variables': 'Specify the values that the model parameters will be set to before the simulation. '
                          'Every line should only have a single parameter with its value.\n\n'
                          'Examples:\n'
                          'sheep-reproduce 5\n'
                          'wolf-reproduce 6',
    'standard_repetitions': 'Specify the number of repetitions that will be run for this configuration.',

    # Experiment/Standard plots
    'config_information': 'Shows the settings of the run configuration in a simple table\n\n'
                          'Usage: To determine which settings, reporters and variables were used without having to '
                          'remember them yourself.',
    'save_results': 'Save the experiment results in a .txt file somewhere on your PC. This will allow you to import '
                    'these results another time so you don\'t need run the model every time you want to use the '
                    'visualisations.',

    # Experiment plots
    'parallel_coordinates': 'Shows vertical axis with the parameters and reporters in a single graph. For each '
                            'scenario, a line is drawn through the parameter and output values to create an easy '
                            'overview of the entire experiment.\n\n'
                            'Usage: To determine the effect of the model parameters on the output of the model. This '
                            'can be used for sensitivity analysis and parameter optimisation.',
    'scatterplot': 'Shows a scatter plot of the specified variables, with a trendline to easily see the correlation '
                   'between an input and output value.\n\n'
                   'Usage: To determine the effect of a model parameter on the output of the model. This '
                   'can be used for sensitivity analysis and parameter optimisation.',
    'scatterplot_variables': 'Specify the values that will be plotted in a scatter plot. The first input (parameter) '
                             'will be plotted on the x-axis and the second input (reporter) will be plotted on the '
                             'y-axis. Make sure to include the double quotes in the text. Every line should only have '
                             'a single parameter-reporter pair and all of them need to be valid within this run '
                             'configuration. Pairs can not be split between lines.\n\n'
                             'Examples:\n'
                             '"sheep-reproduce" "count sheep"\n'
                             '"wolf-reproduce" "count sheep"',
    'heatmap': 'Shows a heatmap of the parameters and reporters, which shows the correlation between all pairs of '
               'variables of the model. \n\n'
               'Usage: To determine the effect of a model parameter on the output of the model. This '
               'can be used for sensitivity analysis and parameter optimisation.',
    '4_metric': 'Specify what metric should be used to merge the data. This metric will be executed for each '
                'repetition within a scenario. After this, the average of these values is taken to obtain the final '
                'value for the scenario that will be plotted. The default selection is average.\n\n',

    # Standard plots
    'timeseries': 'Shows a line plot with the ticks of a simulation on the x-axis and the value of one or more '
                  'reporters on the y-axis.\n\n'
                  'Usage: To determine how the value of a reporter changes during a simulation. This can be used to '
                  'determine whether a specified model configuration achieves the desired results.',
    'boxplot': 'Shows a box plot of all values of one or more reporters during a simulation. The values of all '
               'repetitions are grouped together in a single box plot for each reporter.\n\n'
               'Usage: To determine the variance of the value of a reporter for a specified model configuration '
               'over multiple model runs.',
    'violinplot': 'Shows a violin plot of all values of one or more reporters during a simulation. The values of all '
                  'repetitions are grouped together in a single violin plot for each reporter.\n\n'
                  'Usage: To determine the variance of the value of a reporter for a specified model configuration '
                  'over multiple model runs.',
    'histogram': 'Shows a histogram of the values of one or more reporters at each tick during a simulation.\n\n'
                 'Usage: To determine the frequency of certain reporter values for a specified model configuration '
                 'over multiple model runs',
    'distributionplot': 'Shows the distribution of the values of one or more reporters at each tick during a '
                        'simulation. This is done with a histogram, line curve and a rug plot.\n\n'
                        'Usage: To determine the frequency of certain reporter values for a specified model '
                        'configuration over multiple model runs',
    'distributionplot_indicators': 'Specify which of the three options should be plotted in the visualisation. Any '
                                   'combination of the three checkboxes is valid.',
    '3_metric': 'Specify what metric should be used to merge the data. This metric will be executed for all the data '
                'at each tick, such that the value at each tick can be plotted. The default selection is average.\n\n'
                'Example: If there are 5 repetitions and the values at a certain tick for these are [4, 5, 3, 7, 4], '
                'the following value will be plotted at that tick:\n'
                'Average: 4.6\n'
                'Maximum: 7\n'
                'Minimum: 3',
    'standard_plot_reporters': 'Specify the NetLogo reporters that will be plotted in the graph. Every line should '
                               'only have a single reporter and all of them need to be valid NetLogo '
                               'reporters that were recorded during the simulation. Reporters can not be split between '
                               'lines.',

}
