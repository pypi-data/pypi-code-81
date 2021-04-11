import numpy as np
import multiprocessing as mp

from pysyd import utils
from pysyd.target import Target


def main(args):
    """Runs the SYD-PYpline.

    Parameters
    ----------
    args : argparse.Namespace
        the command line arguments
    """

    args = utils.get_info(args)

    if args.parallel:
        # create the separate, asyncrhonous (nthread) processes
        pool = mp.Pool(args.nthreads)
        result_objects = [pool.apply_async(run, args=(group, args)) for group in args.params['stars']]
        results = [r.get() for r in result_objects]
        pool.close()
        pool.join()    # postpones execution of the next line of code until all processes finish
        count = np.sum(results)
    else:
        count = run(args.params['todo'], args)
      
    # check to make sure that at least one star was successful (count == number of successful executions)   
    if count != 0:
        if args.verbose:
            print('Combining results into single csv file.')
            print()
        # Concatenates output into two files
        utils.scrape_output(args)


def run(stargroup, args, count=0):

    for star in stargroup:
        single = Target(star, args)
        run = single.check_data()
        if run:
            count+=1
            single.run_syd()
    return count