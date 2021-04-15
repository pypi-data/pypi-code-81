"""
"""

import graphviz
import os
import pandas as pd
import uuid
import pickle
import json
import glob
import shutil
import datajoint as dj
import numpy as np
from datajoint.schemas import lookup_class_name
from flask import url_for

from loris import config
from loris.errors import LorisError
from loris.utils import is_manuallookup
from loris.io import string_dump


# TODO deprecated
user_has_permission = config.user_has_permission


def datareader(value):
    """data reader for supported files, otherwise just return the file
    """
    if value.endswith('npy') or value.endswith('npz'):
        value = np.load(value)
    elif value.endswith('csv'):
        value = pd.read_csv(value).to_records(False)
    elif value.endswith('pkl'):
        with open(value, 'rb') as f:
            value = pickle.load(f)
    elif value.endswith('json'):
        with open(value, 'r') as f:
            value = json.load(f)

    return value


def filereader(value):
    """
    Copies filepath to tmp folder with uuid
    """
    if not os.path.exists(value):
        raise LorisError(f"Filepath {value} does not exist.")
    basename = os.path.basename(value)
    basename = f"{uuid.uuid4()}_{basename}"
    dst = os.path.join(config['tmp_folder'], basename)
    assert not os.path.exists(dst)
    shutil.copyfile(value, dst)
    return dst


def get_jsontable(
    data, primary_key, edit_url=None, delete_url=None,
    overwrite_url=None, name=None, load_url=None
):
    """get json table from dataframe
    """

    if primary_key is None:
        pass
    elif len(data) == 0:
        data = pd.DataFrame(
            columns=['_id'] + list(data.columns)
        )
    else:
        _id = pd.Series(
            data[primary_key].to_dict('records')
        ).apply(string_dump)
        _id.name = '_id'
        data = pd.concat([_id, data], axis=1)

    jsontable = {}
    jsontable['delete_url'] = str(delete_url)
    jsontable['edit_url'] = str(edit_url)
    jsontable['load_url'] = str(load_url)
    jsontable['overwrite_url'] = str(overwrite_url)
    jsontable['execute'] = 'True'
    jsontable['id'] = str(name)
    jsontable['head'] = list(data.columns)
    jsontable['data'] = data.values
    return jsontable


def name_lookup(full_name):
    """ Look for a table's class name given its full name. """
    try:
        return config.get_table(full_name, as_string=True)
    except Exception:
        return full_name


def draw_helper(obj=None, type='table', only_essentials=False):
    """
    helper for drawing erds
    """
    # Do not redo when image exists
    if obj is None:
        filename = 'eerrdd'
    elif type == 'table':
        filename = obj.full_table_name
    else:
        filename = obj

    filename = filename + str(only_essentials)

    filepath = os.path.join(config['tmp_folder'], filename)

    # append filename to empty list for removing when refreshing database
    config['_empty'].append(filename)

    filepaths = glob.glob(filepath + '*' + '.svg')
    if len(filepaths) == 1:
        return os.path.split(filepaths[0])[-1]

    # add random string (for rendering purposes on browsers)
    random_string = str(uuid.uuid4())
    filename += random_string
    filepath += random_string

    # rankdir TB?
    # setup of graphviz
    graph_attr = {
        'rankdir': 'LR', 'splines': 'ortho',
        'fontname': 'helvetica'
    }
    node_attr = {
        'style': 'filled, rounded', 'shape': 'record', 'align': 'center',
        'ranksep': '0.1', 'fontsize': '10',
        'penwidth': '1.5', 'height': '0.1', 'fontname': 'helvetica'
    }
    edge_attr = {
        'arrowsize': '0.7',
        'headclip': 'true',
        'penwidth': '1.5'
    }

    node_attrs = {
        dj.Manual: {
            'fillcolor': 'darkgreen',
            'color': 'darkgreen',
            'fontsize': '10',
            'fontcolor': 'white'},
        dj.Computed: {
            'fillcolor': 'darkorchid3',
            'color': 'darkorchid3',
            'fontsize': '10',
            'fontcolor': 'white'},
        dj.Lookup: {
            'fillcolor': 'azure4',
            'color': 'azure4',
            'fontsize': '10',
            'fontcolor': 'white'},
        dj.Imported: {
            'fillcolor': 'navyblue',
            'color': 'navyblue',
            'fontsize': '10',
            'fontcolor': 'white'},
        dj.Part: {
            'fillcolor': 'azure4',
            'color': 'azure4',
            'fontsize': '6',
            'fontcolor': 'white'},
        dj.Settingstable: {
            'fillcolor': 'goldenrod',
            'color': 'goldenrod',
            'fontsize': '6',
            'fontcolor': 'white'},
        dj.AutoComputed: {
            'fillcolor': 'darkorchid4',
            'color': 'darkorchid4',
            'fontsize': '10',
            'fontcolor': 'white'},
        dj.AutoImported: {
            'fillcolor': 'navy',
            'color': 'navy',
            'fontsize': '10',
            'fontcolor': 'white'},
    }

    edge_attrs = {
        dj.Manual: {
            'color': 'darkgreen',
        },
        dj.Computed: {
            'color': 'darkorchid3',
        },
        dj.Lookup: {
            'color': 'azure4',
        },
        dj.Imported: {
            'color': 'navyblue',
        },
        dj.Part: {
            'color': 'azure4',
        },
        dj.Settingstable: {
            'color': 'goldenrod',
        },
        dj.AutoComputed: {
            'color': 'darkorchid4',
        },
        dj.AutoImported: {
            'color': 'navy',
        },
    }

    dot = graphviz.Digraph(
        graph_attr=graph_attr, node_attr=node_attr,
        edge_attr=edge_attr, engine='dot', format='svg')

    def add_node(name, node_attr={}):
        """
        Add a node/table to the current graph (adding subgraphs if needed).
        """

        table_names = dict(
            zip(['schema', 'table', 'subtable'], name.split('.'))
        )
        graph_attr = {
            'color': 'black',
            'label': '<<B>{}</B>>'.format(table_names['schema']),
            'URL': url_for('erd', schema=table_names['schema']),
            'target': '_top',
            'style': 'rounded',
            'penwidth': '3'
        }

        with dot.subgraph(
            name='cluster_{}'.format(table_names['schema']),
            node_attr=node_attr,
            graph_attr=graph_attr
        ) as subgraph:
            subgraph.node(
                name,
                label='{}'.format(name.split('.')[-1]),
                URL=url_for('table', **table_names),
                target='_top', **node_attr
            )
        return name

    def is_essential(name):
        truth = dj.diagram._get_tier(name) in [
            dj.Manual, dj.Computed, dj.Lookup,
            dj.Imported, dj.AutoComputed, dj.AutoImported
        ]

        if truth:
            try:
                schema, table = name_lookup(name).split('.')
                table = getattr(
                    config['schemata'][schema],
                    table
                )
                truth = not (
                    is_manuallookup(table)
                    or (
                        table.full_table_name
                        == config.user_table.full_table_name)
                    or (
                        table.full_table_name
                        == config.group_table.full_table_name)
                    or (
                        table.full_table_name
                        == config.assigned_table.full_table_name)
                    or (
                        schema
                        in config.group_table.proj().fetch()[
                            config['group_name']
                        ]
                    ) or (
                        schema
                        in config.user_table.proj().fetch()[
                            config['user_name']
                        ]
                    )
                )
            except (KeyError, ValueError):
                print('did not check essential table')

        return truth

    if type == 'table':
        root_table = obj
        root_dependencies = root_table.connection.dependencies
        root_dependencies.load()
        root_name = root_table.full_table_name
        root_id = add_node(
            name_lookup(root_name), node_attrs[dj.diagram._get_tier(root_name)]
        )

        # in edges
        for node_name, _ in root_dependencies.in_edges(root_name):
            if dj.diagram._get_tier(node_name) is dj.diagram._AliasNode:
                # renamed attribute
                node_name = list(root_dependencies.in_edges(node_name))[0][0]

            node_id = add_node(
                name_lookup(node_name),
                node_attrs[dj.diagram._get_tier(node_name)]
            )
            dot.edge(
                node_id, root_id,
                **edge_attrs[dj.diagram._get_tier(node_name)]
            )

        # out edges
        for _, node_name in root_dependencies.out_edges(root_name):
            if dj.diagram._get_tier(node_name) is dj.diagram._AliasNode:
                # renamed attribute
                node_name = list(root_dependencies.out_edges(node_name))[0][1]

            node_id = add_node(
                name_lookup(node_name),
                node_attrs[dj.diagram._get_tier(node_name)]
            )
            dot.edge(
                root_id, node_id,
                **edge_attrs[dj.diagram._get_tier(root_name)]
            )
    else:
        dependencies = config['connection'].dependencies
        dependencies.load()
        for root_name in dependencies.nodes.keys():
            try:
                int(root_name)
                continue
            except Exception:
                pass
            schema = root_name.replace('`', '').split('.')[0]
            if obj is None and schema in config['skip_schemas']:
                continue
            if obj is not None and (obj != schema):
                continue
            if only_essentials and not is_essential(root_name):
                continue

            root_id = add_node(
                name_lookup(root_name),
                node_attrs[dj.diagram._get_tier(root_name)]
            )

            for _, node_name in dependencies.out_edges(root_name):
                if dj.diagram._get_tier(node_name) is dj.diagram._AliasNode:
                    # renamed attribute
                    node_name = list(dependencies.out_edges(node_name))[0][1]
                if only_essentials and not is_essential(node_name):
                    continue

                node_id = add_node(
                    name_lookup(node_name),
                    node_attrs[dj.diagram._get_tier(node_name)]
                )
                dot.edge(
                    root_id, node_id,
                    **edge_attrs[dj.diagram._get_tier(root_name)]
                )

    if os.path.exists(filepath):
        os.remove(filepath)
    dot.render(filepath)

    return f'{filename}.svg'
