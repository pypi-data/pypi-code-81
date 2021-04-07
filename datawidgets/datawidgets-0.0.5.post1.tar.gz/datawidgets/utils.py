from datawidgets.imports import *


def convert_single_row_to_series(row: pd.DataFrame):
    if isinstance(row, pd.DataFrame):
        if not len(row) == 1:
            raise ValueError(
                # f"Expected a `Series` or a `DataFrame` with one row, got {len(row)} rows"
                f"Only 1 image must be selected to compute similarity; {len(row)} are currently selected"
            )
        return row.iloc[0]
    else:
        return row


def convert_labels_to_list(label: Union[str, List[str]], split_delimiter=None):
    if isinstance(label, str):
        if split_delimiter is None:
            return [label]
        else:
            return label.split(split_delimiter)
    elif isinstance(label, list):
        return label
    elif isinstance(label, np.ndarray):
        if isinstance(label[0], str):
            return list(label)
    raise TypeError(f"Expected string or list of labels, got {type(label)}")
