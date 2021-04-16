import unittest
from hierarchical_quantifier.reader import read_file, read_file_array
import numpy as np


class ReaderUnitTest(unittest.TestCase):
    files = ['./tests/data/53288-Nocturne_Opus_9_No._2_in_E_Major.mid',
             './tests/data/55352-Sonate_No._14_Moonlight_1st_Movement.mid']
    same_files = ['./tests/data/55352-Sonate_No._14_Moonlight_1st_Movement.mid',
                  './tests/data/55352-Sonate_No._14_Moonlight_1st_Movement.mid']

    file_simple_example = ['./tests/data/simple_example/test_pitch_distribution_C_D_D_C.mid',
                           './tests/data/simple_example/test_pitch_distribution_C_D_D_C_inversed.mid',
                           './tests/data/simple_example/test_pitch_distribution_C_D_D_C_inversed_silence.mid']

    def test_file_reader_file(self):
        ret = read_file('./tests/data/53288-Nocturne_Opus_9_No._2_in_E_Major.mid', 10, force_reset=True)
        self.assertEqual(ret.shape, (10, 12))

    def test_file_reader_neg_resolution(self):
        with self.assertRaises(ValueError):
            read_file('./tests/data/53288-Nocturne_Opus_9_No._2_in_E_Major.mid', 0)

        with self.assertRaises(ValueError):
            read_file('./tests/data/53288-Nocturne_Opus_9_No._2_in_E_Major.mid', -1)

    def test_file_empty(self):
        with self.assertRaises(ValueError):
            read_file('')

    def test_file_not_exist(self):
        with self.assertRaises(FileNotFoundError):
            read_file('./non_existing_file.path.mid')

    def test_file_type_error(self):
        with self.assertRaises(TypeError):
            read_file(10)

    def test_file_non_convertable(self):
        with self.assertRaises(ValueError):
            read_file('./tests/data/non_convertable.mid')

    def test_file_reader_array(self):
        ret = read_file_array(self.files, 10)
        self.assertEqual(ret.shape, (2, 10, 12))

    def test_file_reader_array_with_pickle_type(self):
        with self.assertRaises(ValueError):
            read_file_array(self.files, 10, pickle=True)

        with self.assertRaises(ValueError):
            read_file_array(self.files, 10, force_reset=True)

        with self.assertRaises(ValueError):
            read_file_array(self.files, 10, pickle=True, force_reset=True)

    def test_file_reader_array_with_pickle_read(self):
        ret = read_file_array(self.files, 10, pickle='./tests/data/test_read_file_array_pickle.pkl')
        self.assertEqual(ret.shape, (2, 10, 12))

    def test_file_reader_array_with_pickle_write(self):
        ret = read_file_array(self.files, 10, force_reset='./tests/data/test_read_file_array.pkl')
        self.assertEqual(ret.shape, (2, 10, 12))

    def test_file_reader_array_empty(self):
        with self.assertRaises(ValueError):
            read_file_array([])

    def test_file_reader_array_exception_1_file(self):
        files = ['./tests/data/53288-Nocturne_Opus_9_No._2_in_E_Major.mid', './tests/data/non_convertable.mid',
                 './tests/data/55352-Sonate_No._14_Moonlight_1st_Movement.mid']
        with self.assertRaises(ValueError):
            ret = read_file_array(files, 10)

    def test_pitch_count_single_piece(self):
        ret = read_file(self.file_simple_example[0])
        self.assertEqual(ret.shape, (100, 12))
        self.assertEqual(np.sum(ret, axis=0)[4], 0)  # the pitch class E is never played.

    def test_pitch_count_single_file(self):
        ret = read_file_array(self.file_simple_example)
        self.assertEqual(ret.shape, (3, 100, 12))
        self.assertEqual(np.sum(np.sum(ret, axis=1), axis=0)[4], 0)  # The pitch class E is never player in the corpus.

    def test_pitch_count_highest_count_single_file(self):
        ret = read_file(self.file_simple_example[0])
        self.assertEqual(ret.shape, (100, 12))
        self.assertEqual(np.sum(ret, axis=0).argmax(), 0)  # the highest number of pitch class must be C.
