import click


def global_options(opt):
    opt = click.option('--output-dir', required=False, default='.', help='Output directory, default=.')(opt)
    return opt
