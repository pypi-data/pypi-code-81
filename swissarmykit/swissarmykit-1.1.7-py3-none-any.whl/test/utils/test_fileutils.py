from unittest import TestCase

from swissarmykit.utils.fileutils import FileUtils


class TestFileUtils(TestCase):

    def setUp(self) -> None:
        pass

    def test_get(self):
        print(FileUtils.conf.DIST_PATH)
