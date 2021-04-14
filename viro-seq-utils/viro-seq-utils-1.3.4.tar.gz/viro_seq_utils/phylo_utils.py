#! /usr/bin/env python3

"""
author: Nicolas JEANNE
email: jeanne.n@chu-toulouse.fr
Created on 17 sep. 2020
Copyright (C) PTI CHU Purpan
Version: 1.0.0
"""

import logging
import sys


def get_subtype(seq_id, tree):
    """
     Get the subtype of the sequence ID of interest in a tree. If the subtype of the clade in the tree is a Circulating
     Recombinant Form and starts with digits (i.e: 02_AG), the subtype is written as CRF02-AG, the "_" being also
     replaced by "-".

    :param seq_id: the sequence ID of which subtype is searched.
    :type seq_id: str
    :param tree: the phylogenetic tree.
    :type tree: Bio.Phylo.BaseTree.Tree
    :return: the subtype as a letter for simple subtypes or as CRF<SUBTYPE_NUMBERS>-<SUBTYPE_LETTERS> for Circulating
    Recombinant Forms (CRF), i.e: 02_AG > CRF02-AG.
    :rtype: str
    """
    # Get the clade, with only one leaf of the searched input sequence ID.
    # The first element of the returned iterator.
    try:
        clade_of_input_seq = next(tree.find_clades(seq_id))
    except StopIteration:
        logging.error("{} sequence was not found in the phylogenetic tree:".format(seq_id), exc_info=True)
        sys.exit(1)
    # get the subtype
    subtype = __get_subtype_from_clade(tree, clade_of_input_seq, seq_id, 2, 4)

    # add CRF to the subtype if it starts with a digit: 02_AG > CRF02-AG
    if subtype[0].isdigit():
        subtype = "CRF{}".format(subtype).replace("_", "-")
    return subtype


def __get_subtype_from_clade(phylo_tree, clade, id_to_search, depth_start=2, depth_limit=4):
    """
    Get the list of subtypes in the clade excluding the leaf of interest. If multiple subtypes are present in the clade,
    get the majoritarian subtype, if no majoritarian subtype found get the upper clade and search for the majoritarian
    subtype. The execution is done until it exceeds the depth limit.
    If no subtype is found,  N/D is returned, else the majoritarian subtype is returned.

    :param phylo_tree: the phylogenetic tree.
    :type phylo_tree: Bio.Phylo.BaseTree.Tree
    :param clade: the clade of interest.
    :type clade: Bio.Phylo.BaseTree.Tree
    :param id_to_search: the ID of the leaf to search in the clade.
    :type id_to_search: str
    :param depth_start: the depth of the clades from the leaf id_to_search. Default is -2 for the leaf to search and
    the upper level clade which it belongs.
    :type depth_start: int
    :param depth_limit: the limit of depth to reach in the upper clades, default is 4.
    :type depth_limit: int
    :return: the subtypes in the clade of interest of the other leaves than the leaf of interest.
    :rtype: list
    """

    # check if the list of subtype is odd and if a subtype is majoritarian, else get the upper clade level with the
    # limit set by depth_limit
    for depth in range(depth_start, depth_limit+1):
        # list the leaves of the higher-level clade to find the matching subtype
        clades_list = phylo_tree.get_path(clade)[-depth].get_terminals()
        # get the subtypes of the leaves in a set without the leaf of interest
        subtypes_list = [leaf.name.split(".")[0] for leaf in clades_list if leaf.name != id_to_search]
        subtypes = {sub: subtypes_list.count(sub) for sub in subtypes_list}
        max_count = max(subtypes.values())
        max_subtypes = [k for k, v in subtypes.items() if v == max_count]
        if len(max_subtypes) == 1:
            max_subtype = max_subtypes[0]
            logging.info('Subtype of {} found in clade [{}]'.format(id_to_search, ", ".join(subtypes_list)))
            return max_subtype
        logging.warning("More than one subtype in the clade [{}] and no majoritarian subtype, check the upper "
                        "clade.".format(", ".join(subtypes_list)))
    logging.warning("Limit of depth level reached for the {} subtype reached, subtype set "
                    "as 'N/D'.".format(id_to_search))
    return "N/D"
