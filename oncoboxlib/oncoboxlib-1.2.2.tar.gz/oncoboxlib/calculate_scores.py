import argparse
import logging
from pathlib import Path
from textwrap import dedent

from scipy.stats import ttest_ind
from statsmodels.stats.multitest import multipletests

from oncoboxlib.quant.database import adjust_samples_for_db, load_database
from oncoboxlib.quant.scoring import calc_cnr, calc_pal
from oncoboxlib.quant.scoring.samples import load_samples

logger = logging.getLogger('oncoboxlib')


class BlankLinesHelpFormatter (argparse.HelpFormatter):
    def _split_lines(self, text, width):
        return super()._split_lines(text, width) + ['']


def parse_arguments(argv=None):
    parser = argparse.ArgumentParser(
        description=dedent('''
            Command line tool for calculation of pathway activation level
            according to doi: 10.3389/fgene.2021.617059
        '''),
        formatter_class=BlankLinesHelpFormatter)

    parser.add_argument(
        '--samples-file',
        help=dedent('''
            Table that contains gene expression for cases (or cases and controls).
            Allowed separators: comma, semicolon, tab, space. Compressed (zipped) files are supported as well.
            First column - gene symbol in HGNC format, see genenames.org.
            Others columns - gene expression data for cases or controls.
            Names of case columns should contain "Case", "Tumour", or "Tumor", case insensitive.
            Names of control columns should contain "Control" or "Norm", case insensitive.
            It is supposed that data is already normalized by DESeq2, quantile normalization or other methods.
        '''),
        required=True
    )

    parser.add_argument(
        '--controls-file',
        help=dedent('''
            Optional file that contains controls.
            If provided, cases and controls will be increased by one and normalized by quantile normalization.
        ''')
    )

    parser.add_argument(
        '--samples-format',
        default='ngs counts',
        choices=['ngs counts', 'microarray expression'],
        # help='Samples sequence format'
        help=argparse.SUPPRESS
    )

    parser.add_argument(
        '--norm-averaging',
        default='gmean',
        choices=['gmean', 'mean'],
        # help=dedent('''
        #     Type of norms averaging, "gmean" - geometric mean, "mean" - arithmetic mean.
        # ''')
        help=argparse.SUPPRESS
    )

    parser.add_argument(
        '--ttest',
        action='store_true',
        help=dedent('''
            Include to result a column for unequal variance t-test two-tailed p-values (aka Welch's t-test).
            It is assumed that cases and norms are independent.
            t-test will be performed between all cases and all controls.
        ''')
    )

    parser.add_argument(
        '--fdr-bh',
        action='store_true',
        help='Include to result a column for p-values corrected for FDR using Benjamini/Hochberg method'
    )

    parser.add_argument(
        '--databases-dir',
        help=dedent('''
            Directory that contains pathway databases.
            Databases can be downloaded from https://gitlab.com/oncobox/oncoboxlib/-/blob/master/resources/databases.zip
            (Biocarta 1.123, KEGG Adjusted 1.123, Metabolism 1.123, NCI 1.123, Qiagen 1.123, Reactome 1.123)
        '''),
        required=True
    )
    parser.add_argument(
        '--database-format',
        default='csv',
        choices=['csv', 'xlsx'],
        # help='Type of databases format'
        help=argparse.SUPPRESS
    )
    parser.add_argument(
        '--databases-names',
        default='all',
        help=dedent('''
            Names of databases that are used to calculate PALs.
            "all" means that all database from --databases-dir will be used.
        ''')
    )

    parser.add_argument(
        '--results-file',
        required=False,
        help='Output file that will contain results, "pal.csv" by default'
    )

    args = parser.parse_args(argv[1:] if argv else None)

    if args.fdr_bh and not args.ttest:
        parser.error('--ttest is required when --fdr-bh is set.')

    return args


def main(argv=None):
    args = parse_arguments(argv)

    databases_dir = Path(args.databases_dir)
    if not databases_dir.exists():
        raise ValueError(f'Databases path not found: {args.databases_dir}')

    if args.databases_names == 'all':
        databases_dirs = [d for d in databases_dir.iterdir() if d.is_dir()]
    else:
        databases_dirs = [d for d in databases_dir.iterdir() if d.is_dir() and d.name in args.databases_names]

    if not databases_dirs:
        raise ValueError('Not found any database.')

    # load cases and norms.
    # cases will be quantile normalized when set controls_file
    # samples must include norms when controls_file not set
    samples, case_columns, norm_columns = load_samples(
        args.samples_file, args.controls_file, samples_format='ngs counts')

    if args.ttest:
        if len(case_columns) < 2:
            raise ValueError('t-test requires two or more cases.')
        if len(norm_columns) < 2:
            raise ValueError('t-test requires two or more norms.')

    # get case-to-norm-ratio (cnr)
    # cnr = calc_cnr(samples, norm_columns, args.norm_averaging)
    cnr = calc_cnr(samples, norm_columns, 'gmean')

    # load selected databases
    databases = [load_database(path, 'csv') for path in databases_dirs]

    if args.results_file is None:
        results_file = Path(args.samples_file).absolute().parent / 'pal.csv'
    else:
        results_file = Path(args.results_file)
        results_file.parent.mkdir(exist_ok=True, parents=True)

    joined_pal = None
    for db in databases:
        adjusted_cnr = adjust_samples_for_db(cnr, db, 1.0)
        pal = calc_pal(adjusted_cnr, db.arr, db.gp)
        pal.insert(0, 'database', '{name} {version}'.format(**db.pathway_db))

        if joined_pal is None:
            joined_pal = pal
        else:
            joined_pal = joined_pal.append(pal)

    pvalues = None
    if args.ttest:
        cases_df = joined_pal[case_columns]
        norms_df = joined_pal[norm_columns]
        _, pvalues = ttest_ind(cases_df, norms_df, axis=1)
        joined_pal['pvalue'] = pvalues

    if args.fdr_bh:
        assert args.ttest
        assert pvalues is not None

        ret = multipletests(pvalues, method='fdr_bh')
        _, pvalues_corrected, _, _ = ret
        joined_pal['fdr_bh'] = pvalues_corrected

    joined_pal.to_csv(results_file)

    logger.info(f'Calculation complete. Result -> {results_file}')


if __name__ == '__main__':
    logging_format = '%(asctime)s %(levelname)-8s %(name)-12s: %(message)s'
    logging.basicConfig(level=logging.INFO, format=logging_format)
    # logging.getLogger('oncoboxlib').setLevel(logging.DEBUG)

    main()
