import click

@click.command(name='run_pulls')
@click.option('-i', '--input_file', required=True, help='Path to the input workspace file')
@click.option('-w', '--workspace', default='combWS', help='Name of workspace')
@click.option('-m', '--model_config', default='ModelConfig', help='Name of model config')
@click.option('-d', '--data', default='combData', help='Name of dataset')
@click.option('-p', '--parameter', default='', help='Nuisance parameter(s) to run pulls on.'+\
                                                    'Multiple parameters are separated by commas.'+\
                                                    'Wildcards are accepted.')
@click.option('-x', '--poi', default="", help='POIs to measure')
@click.option('-r', '--profile', default="", help='Parameters to profile')
@click.option('-f', '--fix', default="", help='Parameters to fix')
@click.option('-s', '--snapshot', default="nominalNuis", help='Name of initial snapshot')
@click.option('-o', '--outdir', default="pulls", help='Output directory')
@click.option('-t', '--minimizer_type', default="Minuit2", help='Minimizer type')
@click.option('-a', '--minimizer_algo', default="Migrad", help='Minimizer algorithm')
@click.option('-c', '--num_cpu', type=int, default=1, help='Number of CPUs to use per parameter')
@click.option('-b', '--binned', type=int, default=1, help='Binned likelihood')
@click.option('-q', '--precision', type=float, default=0.001, help='Precision for scan')
@click.option('-e', '--eps', type=float, default=1.0, help='Convergence criterium')
@click.option('-l', '--log_level', default="INFO", help='Log level')
@click.option('--eigen', type=int, default=0, help='Compute eigenvalues and vectors')
@click.option('--strategy', type=int, default=0, help='Default strategy')
@click.option('--fix_cache', type=int, default=1, help='Fix StarMomentMorph cache')
@click.option('--fix_multi', type=int, default=1, help='Fix MultiPdf level 2')
@click.option('--offset', type=int, default=1, help='Offset likelihood')
@click.option('--optimize', type=int, default=2, help='Optimize constant terms')
@click.option('--max_calls', type=int, default=-1, help='Maximum number of function calls')
@click.option('--max_iters', type=int, default=-1, help='Maximum number of Minuit iterations')
@click.option('--parallel', type=int, default=0, help='Parallelize job across different nuisance'+\
                                                      'parameters using N workers.'+\
                                                      'Use -1 for N_CPU workers.')
@click.option('--cache/--no-cache', default=True, help='Cache existing result')
@click.option('--exclude', default="", help='Exclude NPs (wildcard is accepted)')
def run_pulls(input_file, workspace, model_config, data, parameter, poi, profile,
              fix, snapsho, outdir, minimizer_type, minimizer_algo, num_cpu, binned,
              precision, eps, log_level, eigen, strategy, fix_cache, fix_multi,
              offset, optimize, max_calls, max_iters, parallel, cache, exclude):
    """
    Tool for computing the impact of a given NP to a set of POIs
    """
    from quickstats.components import NuisanceParameterPull
    NuisanceParameterPull().run_pulls(input_file, workspace, model_config, data, parameter, poi, profile,
              fix, snapsho, outdir, minimizer_type, minimizer_algo, num_cpu, binned,
              precision, eps, log_level, eigen, strategy, fix_cache, fix_multi,
              offset, optimize, max_calls, max_iters, parallel, cache, exclude)
    
@click.command(name='plot_pulls')
@click.option('-i', '--inputdir', required=True, help='Path to directory containing pull results')
@click.option('-p', '--poi', default=None, help='Parameter of interest for plotting impact')
@click.option('-n', '--n_rank', type=int, default=None, help='Total number of NP to rank')
@click.option('-m', '--rank_per_plot', type=int, default=20, help='Number of NP to show in a single plot')
@click.option('-r', '--ranking', type=int, default=1, help='Rank NP by impact')
@click.option('--threshold', type=float, default=0., help='Filter NP by postfit impact threshold')
@click.option('--show_sigma', type=int, default=1, help='Show one standard deviation pull')
@click.option('--show_prefit', type=int, default=1, help='Show prefit impact')
@click.option('--show_postfit', type=int, default=1, help='Show postfit impact')
@click.option('--sigma_bands', type=int, default=0, help='Draw +-1, +-2 sigma bands')
@click.option('--sigma_lines', type=int, default=1, help='Draw +-1 sigma lines')
@click.option('--shade', type=int, default=1, help='Draw shade')
@click.option('--correlation', type=int, default=1, help='Show correlation impact')
@click.option('--onesided', type=int, default=1, help='Show onesided impact')
@click.option('--theta_max', type=float, default=2, help='Pull range')
@click.option('-y', '--padding', type=int, default=7, help='Padding below plot for texts and legends.' +\
                                                           'NP column height is 1 unit.')
@click.option('-h', '--height', type=float, default=1.0, help='NP column height')
@click.option('-s', '--spacing', type=float, default=0., help='Spacing between impact box')
@click.option('-d', '--display_poi', default=r"$\mu$", help='POI name to be shown in the plot')
@click.option('-t', '--extra_text', default=None, help='Extra texts below the ATLAS label. '+\
                                                       'Use "//" as newline delimiter')
@click.option('--elumi_label', type=int, default=1, help='Show energy and luminosity labels')
@click.option('--ranking_label', type=int, default=1, help='Show ranking label')
@click.option('--energy', type=float, default=13, help='Beam energy')
@click.option('--lumi', type=float, default=139, help='Luminosity')
@click.option('--combine_pdf', type=int, default=1, help='Combine all ranking plots into a single pdf')
@click.option('--outdir', default='ranking_plots', help='Output directory')
@click.option('-o', '--outname', default='ranking', help='Output file name prefix')
@click.option('--style', default='default', help='Plotting style. Built-in styles are "default" and "trex".'+\
                                                 'Specify path to yaml file to set custom plotting style.')
def plot_pulls(inputdir, poi, n_rank, rank_per_plot, ranking, threshold, show_sigma, show_prefit, show_postfit,
               sigma_bands, sigma_lines, shade, correlation, onesided, theta_max, padding, height, spacing,
               display_poi, extra_text, elumi_label, ranking_label, energy, lumi, combine_pdf, outdir,
               outname, style):
    """
    Tool for plotting NP pulls and rankings
    """    
    from quickstats.plots.np_ranking_plot import NPRankingPlot
    ranking_plot = NPRankingPlot(inputdir, poi)
    ranking_plot.plot(show_sigma, show_prefit, show_postfit, sigma_bands, sigma_lines, shade, correlation,
                      onesided, theta_max, padding, height, spacing, display_poi, extra_text, elumi_label, 
                      ranking_label, energy, lumi, n_rank, rank_per_plot, combine_pdf, threshold, ranking,
                      outdir, outname, style)