import numpy as np
from ms2deepscore.plotting import create_confusion_matrix_plot


def test_create_confusion_matrix_plot():
    reference_scores = np.random.random()
create_confusion_matrix_plot(reference_scores, comparison_scores, n_bins=5,
                                 ref_score_name="Tanimoto similarity", compare_score_name="MS2DeepScore",
                                 max_square_size=5000)