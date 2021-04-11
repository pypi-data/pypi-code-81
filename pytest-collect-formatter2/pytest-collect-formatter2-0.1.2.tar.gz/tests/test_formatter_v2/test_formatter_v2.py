import allure
import pytest


class TestFormatter:
    # hhh
    def test_inside_class(self):
        pass

    @pytest.mark.parametrize('tet_id', [1, 2, 3, 4])
    def test_inside_class_parametrize(self, tet_id):
        pass


def test_outside_of_class():
    """
    hello name
    :return:
    """
    pass
