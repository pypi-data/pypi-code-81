"""Module load and transform example dataset"""
from collections import Counter
from pathlib import Path
from typing import List, Tuple

import pandas as pd
import sklearn


def load_example_dataset() -> Tuple[List[str], List[str]]:
    """Load a dataset for multiclass classification"""
    local_path = Path(".").resolve()
    local_path = local_path.joinpath("files/example")

    infos_file = local_path.joinpath("pdb_data_no_dups.csv")
    seq_file = local_path.joinpath("pdb_data_seq.csv")

    assert (
        infos_file.is_file() and seq_file.is_file()
    ), "CSV file not available in data/files/examples"

    df = (
        pd.read_csv(infos_file)
        .merge(pd.read_csv(seq_file), how="inner", on="structureId")
        .drop_duplicates(["sequence"])
    )

    # Filter on null value and protein type
    df = df[[isinstance(c, str) for c in df.classification.values]]
    df = df[[isinstance(c, str) for c in df.sequence.values]]
    df = df[df.macromoleculeType_x == "Protein"]

    # Select top 10 most common protein
    counter = Counter(df.classification)
    sorted_classes = counter.most_common()[:10]
    classes = [c[0] for c in sorted_classes]
    df = df[[c in classes for c in df.classification]]

    X = df.sequence.values.tolist()
    y = df.classification.values.tolist()

    return X, y


if __name__ == "__main__":
    X, y = load_example_dataset()
    print(X[:12], y[12])
