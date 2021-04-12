import os
import pandas as pd
import numpy as np
import yaml
from tqdm import tqdm
from jinja2 import Environment, FileSystemLoader, select_autoescape
import argparse

parser = argparse.ArgumentParser(description='produce html files from csv and jinja')
parser.add_argument('config',
                    help= 'configuration for mail merging csv into html',
                    type = str)
args = parser.parse_args()

def populate_jinja_template(pk, template, filename, data, directories):
    """
    Takes inputs, and creates an html file based on a template.
    """

    # Step 1) move up a directory Level
    # Step 2) ensure an output directory is created.
    # Step 3) Ensure each directory type is created.
    # Step 4) Create output file_path.
    # Step 5) Then create render in directory.

    # Step 1
    this_dir = os.path.dirname(os.path.abspath(__file__))

    # Step 2
    path = this_dir + 'html'

    if not os.path.exists(path):
        os.makedirs(path)

    # Step 3
    for directory in directories:
        loc = data[directory].astype(str).unique().tolist()[0]
        if not os.path.exists(path+"/"+loc):
            os.makedirs(path+"/"+loc)
        path = path+"/"+loc

    # Step 4
    file_loc = path + f'/{filename}.html'

    env = Environment(loader=FileSystemLoader(this_dir, followlinks = True),
                      autoescape=select_autoescape(['html', 'xml']))

    # Converting data from dataframe form to dict form for jinja2 template
    template_data = data.to_dict('list')
    for key, value in template_data.items():
        template_data[key] = value[0]

    # Step 5
    env.get_template(template)\
        .stream(template_data)\
        .dump(file_loc)

class Document():

    def __init__(self, pk, data, config):

        self.config = config
        self.primary_key = pk

        # The head method should not be necessary if data is unique
        self.data = data.query("pk == @self.primary_key").head(1)

        self.filename = self.create_filename(self.data, config["filename_columns"])
        self.directories = config["output_folders"]

        self.template = config["template"]

    def create_render(self):
        """
        Assembles the data and creates the HTML report cards for each recipient.
        """

        card_dat = {
                "pk": self.primary_key,
                "template": self.template,
                "directories": self.directories,
                "filename": self.filename,
                "data": self.data
                }

        populate_jinja_template(**card_dat)

    def create_filename(self, data, columns):

        initial_name = columns[0]

        data["filename"] = data[initial_name].astype(str)

        if columns[1:]:
            for col in columns[1:]:
                data["filename"] = data["filename"] + "_" + data[col].astype(str)

        name = data["filename"].unique().tolist()[0]

        return name

def fix_columns(dataframe):
    """
    Takes a dataframe and fixes the column names by (1) making all lowercase,
    (2) removing non-alphanumeric characters, and (3) replacing spaces with
    an underscore.
    """
    cols = dataframe.columns
    cols = [col.lower() for col in cols]
    cols = [re.sub(r'[^\w\s\d]', '', col) for col in cols]
    cols = [re.sub(r'\s', '_', col) for col in cols]
    dataframe.columns = cols

    return dataframe

def process_data(config):
    """
    Takes specifications in config file to assemble dataframe from data in data directory
    and generate a primary key used to create the letters.
    """

    # Making path to data in the sub-directory
    data_path = config["data"]

    # Reading in the data raw
    raw_data = pd.read_csv(data_path)

    # Constructing the primary key used to generate individual letters
    # 1) Turn identifier column values into strings
    # 2) Concatenate identifier column values to create unique pk
    # raw_data[config["identifier_columns"]] = raw_data[config["identifier_columns"]].astype(str)
    raw_data["pk"] = raw_data[config["identifier_columns"][0]].astype(str)
    if len(config["identifier_columns"]) > 1:
        for col in config["identifier_columns"][1:]:
            raw_data["pk"] = raw_data["pk"] ++ raw_data[col].astype(str)

    raw_data = raw_data.sort_values(by = config["sort"])

    return raw_data

def process_batch(args):
    """
    Main Function of the Regents Generation Script

    1. Reads 'regents_config.yml' file for configurations
    2. Collects & cleans data according to configuration specifications
    3. Generates unique list of letters to be generated
    4. Loops through generation function generating letters
    """

    with open(args.config) as yml:
        config = yaml.load(yml, Loader = yaml.BaseLoader)

    all_data = process_data(config)

    docs = all_data["pk"].unique().tolist()

    def generate_doc(doc):
        dat = all_data.copy()
        con = config.copy()
        doc = Document(doc, dat, con)
        doc.create_render()

    for doc in tqdm(docs):
        generate_doc(doc)

def render(args):
    process_batch(args)

if __name__ == "__main__":
    render(args)
