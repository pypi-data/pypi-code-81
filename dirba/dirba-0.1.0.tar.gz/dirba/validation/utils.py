import logging
import warnings
from typing import List, Tuple

from dirba.models.abc import Predict, BinaryPredict, CategoryId


def multi_categorical_to_single(true_features: List[List[BinaryPredict]],
                                predicted_features: List[List[Predict]]) -> Tuple[List[CategoryId], List[CategoryId]]:
    """
    Преобразует оценки из мульикатегориальных в подготовленные оценки с категориями
    :param predicted_features: список оценок по материалам
    :return:
    """
    logger = logging.getLogger('categorical_to_single')

    def is_correct(true_scores: List[BinaryPredict]) -> bool:
        if len(true_scores) > 1 or len(true_scores) == 0:
            return False
        return True

    skipped = 0
    true_transformed = []
    predicted_transformed = []
    for true_row, predicted_row in zip(true_features, predicted_features):
        true_scores = list(filter(lambda val: val.score, true_row))
        if not is_correct(true_scores):
            skipped += 1
            logger.warning(f"Wrong data in dataset true values. Only 1 target category allowed, but got: {true_row}")
            continue

        max_true_score = max(true_scores, key=lambda val: val.score)
        true_category = max_true_score.category

        max_predicted_score = max(predicted_row, key=lambda val: val.score)
        predicted_category = max_predicted_score.category

        true_transformed.append(true_category)
        predicted_transformed.append(predicted_category)

    if skipped:
        warnings.warn(f'Skipped {skipped} values via translating to single category. To see the rows enable WARN level logging')

    return true_transformed, predicted_transformed


def predict_to_values(true_features: List[List[BinaryPredict]],
                      predicted_features: List[List[Predict]]) -> Tuple[List[List[int]], List[List[float]]]:
    """
    Преобразует значения из объектов оценок в значения, с сортировкой по классам
    :return:
    """
    true_values = [[i.score for i in sorted(row, key=lambda val: val.category)] for row in true_features]
    predicted_values = [[i.score for i in sorted(row, key=lambda val: val.category)] for row in predicted_features]
    return true_values, predicted_values
