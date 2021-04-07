import random
import string

from graphbrain import hedge
from graphbrain.constants import coref_pred
from graphbrain.constants import coref_set_id_key
from graphbrain.constants import main_coref_pred
from graphbrain.op import apply_ops
from graphbrain.op import create_op


def _new_coref_id():
    chars = string.ascii_lowercase + string.digits
    # Note: the size of the id can be increased to reduce the probability
    # of collision.
    return ''.join(random.choice(chars) for i in range(7))


def _set_coref_id_op(hg, edge, coref_id):
    attributes = {coref_set_id_key: coref_id}
    return create_op(edge, optype='set_attributes', attributes=attributes)


def _change_coref_id_ops(hg, edge, coref_id):
    for coref in coref_set(hg, edge):
        yield _set_coref_id_op(hg, coref, coref_id)


def _update_main_coref_ops(hg, edge):
    cref_id = coref_id(hg, edge)
    corefs = coref_set(hg, edge)

    best_coref = None
    best_degree = -1
    for coref in corefs:
        d = hg.degree(coref)
        if d > best_degree:
            best_degree = d
            best_coref = coref

    coref_edge = hedge((main_coref_pred, cref_id, best_coref))
    if not hg.exists(coref_edge):
        old = set(hg.search('({} {} *)'.format(main_coref_pred, cref_id)))
        for old_edge in old:
            # hg.remove(old_edge)
            # print('&&&')
            # print(old_edge)
            yield create_op(old_edge, optype='remove')
        # hg.add(coref_edge, primary=False)
        yield create_op(coref_edge, primary=False)


def coref_set(hg, edge, corefs=None):
    """Returns the set of coreferences that the given edge belongs to."""
    if corefs is None:
        corefs = {edge}
    for coref_edge in hg.edges_with_edges((hedge(coref_pred), edge)):
        if len(coref_edge) == 3 and coref_edge[0].to_str() == coref_pred:
            for item in coref_edge[1:]:
                if item not in corefs:
                    corefs.add(item)
                    coref_set(hg, item, corefs)
    return corefs


def are_corefs(hg, edge1, edge2, corefs=None):
    """Checks if the two given edges are coreferences."""
    if corefs is None:
        corefs = {edge1}
    for coref_edge in hg.edges_with_edges((hedge(coref_pred), edge1)):
        if len(coref_edge) == 3 and coref_edge[0].to_str() == coref_pred:
            for item in coref_edge[1:]:
                if item not in corefs:
                    if item == edge2:
                        return True
                    corefs.add(item)
                    if are_corefs(hg, item, edge2, corefs):
                        return True
    return False


def coref_id(hg, edge):
    """Returns the coreference identifier of the edge."""
    return hg.get_str_attribute(edge, coref_set_id_key)


def main_coref_from_id(hg, cref_id):
    """Returns main edge in the coreference set for the given identifier."""
    for coref_edge in hg.search('({} {} *)'.format(main_coref_pred,
                                                   cref_id)):
        return coref_edge[2]
    return None


def main_coref(hg, edge):
    """Returns main edge for the coreference set that the given edge
    belongs to.
    """
    cref_id = coref_id(hg, edge)
    if cref_id is None:
        return edge
    return main_coref_from_id(hg, cref_id)


def make_corefs_ops(hg, edge1, edge2):
    # print('\n### make_corefs_ops {} {}'.format(edge1, edge2))
    cref_id_1 = coref_id(hg, edge1)
    cref_id_2 = coref_id(hg, edge2)

    if cref_id_1 is None:
        if cref_id_2 is None:
            new_cref_id = _new_coref_id()
        else:
            new_cref_id = cref_id_2
    elif cref_id_2 is None:
        new_cref_id = cref_id_1
    else:
        count1 = len(coref_set(hg, edge1))
        count2 = len(coref_set(hg, edge2))
        if count2 > count1:
            new_cref_id = cref_id_2
        else:
            new_cref_id = cref_id_1

    update = False
    if cref_id_1 != new_cref_id:
        for op in _change_coref_id_ops(hg, edge1, new_cref_id):
            yield op
        update = True
    if cref_id_2 != new_cref_id:
        for op in _change_coref_id_ops(hg, edge2, new_cref_id):
            yield op
        update = True

    # hg.add((coref_pred, edge1, edge2), primary=False)
    yield create_op((coref_pred, edge1, edge2), primary=False)

    if update:
        for op in _update_main_coref_ops(hg, edge1):
            yield op


def make_corefs(hg, edge1, edge2):
    """Make the two given edges belong to the same corefernce set.

    This may trigger further updates to maintain consistency, such as
    merging existing coreference sets and recomputing the main edge of
    a coreference set.
    """
    apply_ops(hg, make_corefs_ops(hg, edge1, edge2))
