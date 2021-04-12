import argparse
from .convert import convert


def run_azyc():
    p = argparse.ArgumentParser()
    p.add_argument("--input", "-i", default="deployment-params.yml",
                   help='Path to yml file containing the parameter definition. (Default: "deployment-params.yml")')
    p.add_argument("--output", "-o", default="template-parameters.json",
                   help='Path to output file that is written. (Default: "template-parameters.json")')
    p.add_argument("--param", action='append',
                   type=lambda kv: kv.split("="), dest='extra',
                   help='Add extra parameters. that will be added to the file. overwrite parameters specified in the yml file. Can be called multiple times. Example: "--param suffix=test --param foo=bar"')
    args = p.parse_args()
    extra_params = dict(args.extra) if args.extra != None else dict()
    convert(args.input, args.output, extra_params)
