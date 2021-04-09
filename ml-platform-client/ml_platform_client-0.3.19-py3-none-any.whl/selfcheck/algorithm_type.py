from enum import Enum


class AlgorithmType(Enum):
    text_classification = 1
    text_sequence_labeling = 2
    text_cluster = 3
    text_generation = 4
    text_custom = 5
    relation_extraction = 6
