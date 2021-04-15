#!/usr/bin/env python3
import argparse
import json
import os
import shutil

import jinja2
import yaml


def build(path):
    data = {}

    data_yaml = os.path.join(os.getcwd(), 'data.yaml')
    if os.path.exists(data_yaml):
        with open(data_yaml) as f:
            data.update(yaml.load(f.read(), Loader=yaml.FullLoader))

    data_yaml = os.path.join(path, 'data.yaml')
    if os.path.exists(data_yaml):
        with open(data_yaml) as f:
            data.update(yaml.load(f.read(), Loader=yaml.FullLoader))

    build_path = os.path.join(os.getcwd(), "build")
    print(build_path)
    if os.path.exists(build_path):
        shutil.rmtree(build_path)
    shutil.copytree(path, build_path)

    for root, subFolders, files in os.walk(build_path):
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath=root))
        for file in files:
            full_path = os.path.join(root, file)
            if ".sub." in full_path:
                # print(f"template: {full_path}")
                template = env.get_template(file)
                output = template.render(data=data).strip()
                output_path = full_path.replace(".sub.", ".")
                with open(output_path, 'w+') as f:
                    f.write(output)
                os.remove(full_path)


def main():
    parser = argparse.ArgumentParser(prog='subtheme')
    parser.add_argument('path', type=str, help='', default='.')
    # parser.add_argument('--data', type=str, help='', default='.')

    args = parser.parse_args()

    build(args.path)


if __name__ == "__main__":
    main()
