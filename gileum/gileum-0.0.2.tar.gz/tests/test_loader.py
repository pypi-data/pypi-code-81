from os.path import basename, join
import unittest

from gileum.loader import (
    list_glmfiles,
    load_glms_at,
    load_glms_in,
)
from gileum.manager import (
    GileumManager,
    init_glm_manager,
    get_glm,
    _reset_glm_manager,
)
from gileum.test import MockGileum

from . import DIR_RES, FILE_SETTING


TEST_NAME = "unittest@gileum"
DEVELOPER_NAME = "jjj999"
GLM_NAME = "main"


class TestLoader(unittest.TestCase):

    def setUp(self) -> None:
        _reset_glm_manager()
        init_glm_manager(GileumManager())

    def test_list_glmfiles(self) -> None:
        result = list_glmfiles(DIR_RES)
        self.assertEqual(len(result), 1)

        glm_file = result[0]
        self.assertTrue(basename(glm_file), "mock_setting.glm.py")

    def assertGileum(self, glm: MockGileum) -> None:
        self.assertEqual(glm.test_name, TEST_NAME)
        self.assertEqual(glm.developer_name, DEVELOPER_NAME)
        self.assertIsInstance(glm.current_time, float)
        self.assertEqual(glm.glm_name, GLM_NAME)

    def test_load_glms_at(self) -> None:
        load_glms_at(join(DIR_RES, FILE_SETTING))
        glm = get_glm(GLM_NAME, MockGileum)
        self.assertGileum(glm)

    def test_load_glms_in(self) -> None:
        load_glms_in(DIR_RES)
        glm = get_glm(GLM_NAME, MockGileum)
        self.assertGileum(glm)


if __name__ == "__main__":
    unittest.main()