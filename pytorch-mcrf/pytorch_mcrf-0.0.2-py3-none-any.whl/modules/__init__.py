import math
from typing import Dict, List, Optional, Tuple, Union

import torch


def allowed_transitions(constraint_type: str, labels: Dict[int, str]) -> List[Tuple[int, int]]:
    """
    Given labels and a constraint type, returns the allowed transitions. It will
    additionally include transitions for the start and end states, which are used
    by the conditional random field.
    # Parameters
    constraint_type : `str`, required
        Indicates which constraint to apply. Current choices are
        "BIO", "IOB1", "BIOUL", and "BMES".
    labels : `Dict[int, str]`, required
        A mapping {label_id -> label}.
    # Returns
    `List[Tuple[int, int]]`
        The allowed transitions (from_label_id, to_label_id).
    """
    num_labels = len(labels)
    start_tag = num_labels
    end_tag = num_labels + 1
    labels_with_boundaries = list(labels.items()) + [(start_tag, "START"), (end_tag, "END")]

    allowed = []
    for from_label_index, from_label in labels_with_boundaries:
        if from_label in ("START", "END"):
            from_tag = from_label
            from_entity = ""
        else:
            from_tag = from_label[0]
            from_entity = from_label[1:]
        for to_label_index, to_label in labels_with_boundaries:
            if to_label in ("START", "END"):
                to_tag = to_label
                to_entity = ""
            else:
                to_tag = to_label[0]
                to_entity = to_label[1:]
            if is_transition_allowed(constraint_type, from_tag, from_entity, to_tag, to_entity):
                allowed.append((from_label_index, to_label_index))
    return allowed


def is_transition_allowed(
    constraint_type: str, from_tag: str, from_entity: str, to_tag: str, to_entity: str
):
    """
    Given a constraint type and strings `from_tag` and `to_tag` that
    represent the origin and destination of the transition, return whether
    the transition is allowed under the given constraint type.
    # Parameters
    constraint_type : `str`, required
        Indicates which constraint to apply. Current choices are
        "BIO", "IOB1", "BIOUL", and "BMES".
    from_tag : `str`, required
        The tag that the transition originates from. For example, if the
        label is `I-PER`, the `from_tag` is `I`.
    from_entity : `str`, required
        The entity corresponding to the `from_tag`. For example, if the
        label is `I-PER`, the `from_entity` is `PER`.
    to_tag : `str`, required
        The tag that the transition leads to. For example, if the
        label is `I-PER`, the `to_tag` is `I`.
    to_entity : `str`, required
        The entity corresponding to the `to_tag`. For example, if the
        label is `I-PER`, the `to_entity` is `PER`.
    # Returns
    `bool`
        Whether the transition is allowed under the given `constraint_type`.
    """

    if to_tag == "START" or from_tag == "END":
        # Cannot transition into START or from END
        return False

    if constraint_type == "BIOUL":
        if from_tag == "START":
            return to_tag in ("O", "B", "U")
        if to_tag == "END":
            return from_tag in ("O", "L", "U")
        return any(
            [
                # O can transition to O, B-* or U-*
                # L-x can transition to O, B-*, or U-*
                # U-x can transition to O, B-*, or U-*
                from_tag in ("O", "L", "U") and to_tag in ("O", "B", "U"),
                # B-x can only transition to I-x or L-x
                # I-x can only transition to I-x or L-x
                from_tag in ("B", "I") and to_tag in ("I", "L") and from_entity == to_entity,
            ]
        )
    elif constraint_type == "BIO":
        if from_tag == "START":
            return to_tag in ("O", "B")
        if to_tag == "END":
            return from_tag in ("O", "B", "I")
        return any(
            [
                # Can always transition to O or B-x
                to_tag in ("O", "B"),
                # Can only transition to I-x from B-x or I-x
                to_tag == "I" and from_tag in ("B", "I") and from_entity == to_entity,
            ]
        )
    elif constraint_type == "IOB1":
        if from_tag == "START":
            return to_tag in ("O", "I")
        if to_tag == "END":
            return from_tag in ("O", "B", "I")
        return any(
            [
                # Can always transition to O or I-x
                to_tag in ("O", "I"),
                # Can only transition to B-x from B-x or I-x, where
                # x is the same tag.
                to_tag == "B" and from_tag in ("B", "I") and from_entity == to_entity,
            ]
        )
    elif constraint_type == "BMES":
        if from_tag == "START":
            return to_tag in ("B", "S")
        if to_tag == "END":
            return from_tag in ("E", "S")
        return any(
            [
                # Can only transition to B or S from E or S.
                to_tag in ("B", "S") and from_tag in ("E", "S"),
                # Can only transition to M-x from B-x, where
                # x is the same tag.
                to_tag == "M" and from_tag in ("B", "M") and from_entity == to_entity,
                # Can only transition to E-x from B-x or M-x, where
                # x is the same tag.
                to_tag == "E" and from_tag in ("B", "M") and from_entity == to_entity,
            ]
        )
    else:
        raise ValueError(f"Unknown constraint type: {constraint_type}")


def get_transition_mask_mat(
    scheme: str,
    id2label: Dict[int, str],
    return_start_end_transitions: Optional[bool] = True
) -> Union[torch.Tensor, Tuple]:
    r"""get transition mask matrix for masked CRF

    Args:
        scheme: tagging label scheme, choices are "BIO", "IOB1", "BIOUL", and "BMES"
        id2label: tag id to tag name. e.g. {0: 'O', 1: 'B-PER', ...}
        return_start_end_transitions: whether to return start and end transition vectors

    Returns:
        transition matrix
        start transition vector if `return_start_end_transitions`
        end transition vector if `return_start_end_transitions`
    """
    allowed_with_start_end = allowed_transitions(scheme, id2label)
    return get_transition_mask_mat_from_allowed(len(id2label), allowed_with_start_end, return_start_end_transitions)


def get_transition_mask_mat_from_allowed(
        num_tags: int,
        allowed_with_start_end: List[Tuple],
        return_start_end_transitions: Optional[bool] = True):
    r"""get transition mask matrix for masked CRF given allowed_transitions

    Args:
        num_tags: number of tags (despite START and END)
        allowed_with_start_end: allowed transition tuples, got from `allowed_transitions()`
        return_start_end_transitions: whether to return start and end transition vectors

    Returns:
        transition matrix
        start transition vector if `return_start_end_transitions`
        end transition vector if `return_start_end_transitions`
    """
    trans_mask = -torch.ones(num_tags, num_tags, dtype=torch.float)
    start_mask = -torch.ones(num_tags, dtype=torch.float)
    end_mask = -torch.ones(num_tags, dtype=torch.float)

    start_tag_idx = num_tags
    end_tag_idx = num_tags + 1

    for from_label_index, to_label_index in allowed_with_start_end:
        if from_label_index == start_tag_idx and to_label_index == end_tag_idx:
            continue
        if from_label_index == start_tag_idx:
            start_mask[to_label_index] = 1.0
        elif to_label_index == end_tag_idx:
            end_mask[from_label_index] = 1.0
        else:
            trans_mask[from_label_index, to_label_index] = 1.0

    trans_mask *= 100
    start_mask *= 100
    end_mask *= 100

    if return_start_end_transitions:
        return trans_mask, start_mask, end_mask
    else:
        return trans_mask


from .plain import PlainCRF
from .constraint import ConstraintCRF
from .masked import MaskedCRF
