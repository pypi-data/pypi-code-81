import unittest
from hierarchical_quantifier.quantifier import get_mi_scape, get_pitch_scape, get_join_pcd, get_pcd, reduce_scape_2d, \
    get_kld_scape, reduce_scape_horizontale, reduce_1d, bootstrap
from hierarchical_quantifier.reader import read_file_array, read_file
import numpy as np


class QuantifierUnitTest(unittest.TestCase):
    files = ['./tests/data/53288-Nocturne_Opus_9_No._2_in_E_Major.mid',
             './tests/data/55352-Sonate_No._14_Moonlight_1st_Movement.mid']
    same_files = ['./tests/data/55352-Sonate_No._14_Moonlight_1st_Movement.mid',
                  './tests/data/55352-Sonate_No._14_Moonlight_1st_Movement.mid']

    file_simple_example = ['./tests/data/simple_example/test_pitch_distribution_C_D_D_C.mid',
                           './tests/data/simple_example/test_pitch_distribution_C_D_D_C_inversed.mid',
                           './tests/data/simple_example/test_pitch_distribution_C_D_D_C_inversed_silence.mid']

    def test_get_mi_scape_wrong_type(self):
        with self.assertRaises(TypeError):
            get_mi_scape(0, 'true')  # test wrong input type

    def test_get_mi_scape_wrong_number_pitch_class(self):
        with self.assertRaises(ValueError):
            get_mi_scape(np.ones((5, 50, 10)))  # test wrong input type

    def test_get_mi_scape_not_a_corpus(self):
        with self.assertRaises(ValueError):
            ret = read_file_array([self.file_simple_example[0]])
            get_mi_scape(ret)

    def test_get_mi_scape_shape(self):
        ret = get_mi_scape(read_file_array(self.file_simple_example))
        self.assertEqual(ret.shape, (100, 100))

    def test_get_mi_scape_nbr_dim(self):
        with self.assertRaises(ValueError):
            get_mi_scape(np.ones((5, 10, 12, 3)))

    def test_get_mi_scape_shape_custom(self):
        ret = get_mi_scape(read_file_array(self.file_simple_example, 10))
        self.assertEqual(ret.shape, (10, 10))

    def test_get_mi_scape_zero_diagonal(self):
        ret = get_mi_scape(read_file_array(self.file_simple_example))
        self.assertEqual(sum(ret.diagonal()), 0)

    def test_get_mi_scape_silence_count_corpus_diagonal(self):
        silence_counts = np.zeros((5, 10, 12))  # silence corpus
        temp = get_mi_scape(silence_counts, False)  # compare the same index.
        self.assertTrue((temp.diagonal() == np.log2(12)).all())

    def test_get_mi_scape_silence_count_corpus(self):
        silence_counts = np.zeros((5, 10, 12))  # silence corpus
        temp = get_mi_scape(silence_counts)  # compare the same index.
        np.testing.assert_almost_equal(temp, np.zeros((10, 10)))  # pieces are silence, the mutual information is zero.

    def test_get_mi_scape_same_piece_corpus(self):
        corp1 = ['./tests/data/simple_example/test_pitch_distribution_C_D_D_C.mid',
                 './tests/data/simple_example/test_pitch_distribution_C_D_D_C.mid']

        corp2 = ['./tests/data/simple_example/test_pitch_distribution_C_D_D_C.mid',
                 './tests/data/simple_example/test_pitch_distribution_C_D_D_C.mid',
                 './tests/data/simple_example/test_pitch_distribution_C_D_D_C.mid']
        sample = 20
        ret1 = get_mi_scape(read_file_array(corp1, sample))
        ret2 = get_mi_scape(read_file_array(corp2, sample))

        np.testing.assert_almost_equal(ret1, ret2)

    def test_get_mi_scape_negatif_count(self):
        temp = read_file_array(self.file_simple_example, 10)
        temp[0, 5, 1:3] = -1  # remplace with negativ counts
        with self.assertRaises(ValueError):
            get_mi_scape(temp)

    def test_get_mi_scape_single_note_piece(self):
        shape_piece = (10, 12)
        p1 = np.zeros(shape_piece)
        p1[:, 0] = 1  # all C

        p2 = np.zeros(shape_piece)
        p2[:, 2] = 1  # all D

        p3 = np.zeros(shape_piece)
        p3[:, 4] = 1  # all E

        p4 = np.zeros(shape_piece)
        p4[:, 7] = 1  # all G
        corpus = np.vstack([p1[None], p2[None], p3[None], p4[None]])
        self.assertTrue((get_mi_scape(corpus, False) == 2).all())

    def test_get_mi_scape_high_mi_at_end(self):
        shape_piece = (10, 12)
        p1 = np.zeros(shape_piece)
        p1[0:2, 0] = 1  # all C
        p1[8:10, 0] = 1  # all C

        p2 = np.zeros(shape_piece)
        p2[0:2, 2] = 1  # all D
        p2[8:10, 2] = 1  # all D

        p3 = np.zeros(shape_piece)
        p3[0:2, 4] = 1  # all E
        p3[8:10, 4] = 1  # all E

        p4 = np.zeros(shape_piece)
        p4[0:2, 7] = 1  # all G
        p4[8:10, 7] = 1  # all G

        corpus = np.vstack([p1[None], p2[None], p3[None], p4[None]])

        ret = get_mi_scape(corpus)
        # short term relationship
        self.assertEqual(ret[0, 1], ret[-2, -1])

        # long term relationship
        self.assertEqual(ret[0, -1], ret[1, -2])

    def test_get_pitch_scape_wrong_type(self):
        with self.assertRaises(TypeError):
            get_pitch_scape('piece')

    def test_get_pitch_scape_not_matching_pitch_class(self):
        with self.assertRaises(ValueError):
            get_pitch_scape(np.ones((10, 11)))

    def test_get_pitch_scape_negative_counts(self):
        temp = np.ones((10, 12))
        temp[0, :] = -1
        with self.assertRaises(ValueError):
            get_pitch_scape(temp)

    def test_get_pitch_scape_mismatch_nbr_dim(self):
        with self.assertRaises(ValueError):
            get_pitch_scape(np.ones((10, 12, 4)))

    def test_get_pitch_scape_return_shape(self):
        self.assertEqual(get_pitch_scape(read_file(self.file_simple_example[0], 10)).shape, (10, 10, 12))

    def test_get_pitch_scape_silence_count(self):
        silence_count = np.zeros((10, 12))

        to_compare = np.zeros((10, 10, 12))
        to_compare[np.triu_indices(10)] = 1 / 12

        np.testing.assert_almost_equal(get_pitch_scape(silence_count), to_compare)

    def test_get_pcd(self):
        shape_piece = (10, 12)
        p1 = np.zeros(shape_piece)
        p1[0:2, 0] = 1  # all C
        p1[8:10, 0] = 1  # all C

        p2 = np.zeros(shape_piece)
        p2[0:2, 2] = 1  # all D
        p2[8:10, 2] = 1  # all D

        p3 = np.zeros(shape_piece)
        p3[0:2, 4] = 1  # all E
        p3[8:10, 4] = 1  # all E

        p4 = np.zeros(shape_piece)
        p4[0:2, 7] = 1  # all G
        p4[8:10, 7] = 1  # all G

        corpus = np.vstack([p1[None], p2[None], p3[None], p4[None]])

        pcd = get_pcd(corpus)
        self.assertEqual(pcd.shape, (10, 12))

        np.testing.assert_almost_equal(pcd[0, :], np.asarray([0.25, 0, 0.25, 0, 0.25, 0, 0, 0.25, 0, 0, 0, 0]))

    def test_get_jpcd(self):
        shape_piece = (10, 12)
        p1 = np.zeros(shape_piece)
        p1[0:2, 0] = 1  # all C
        p1[8:10, 0] = 1  # all C

        p2 = np.zeros(shape_piece)
        p2[0:2, 2] = 1  # all D
        p2[8:10, 2] = 1  # all D

        p3 = np.zeros(shape_piece)
        p3[0:2, 4] = 1  # all E
        p3[8:10, 4] = 1  # all E

        p4 = np.zeros(shape_piece)
        p4[0:2, 7] = 1  # all G
        p4[8:10, 7] = 1  # all G

        corpus = np.vstack([p1[None], p2[None], p3[None], p4[None]])

        jpcd = get_join_pcd(corpus)

        self.assertEqual(jpcd.shape, (10, 10, 12, 12))
        self.assertEqual(jpcd[0, 0, 0, 0], 0.25)
        self.assertEqual(jpcd[0, 0, 2, 2], 0.25)
        self.assertEqual(jpcd[0, 0, 2, 0], 0)
        self.assertAlmostEqual(jpcd[5, 6, 3, 3], 1 / 144)

    def test_get_kld_scape_wrong_input(self):
        ps_wrong_type = np.ones((10, 12))
        with self.assertRaises(TypeError):
            get_kld_scape('ps')
        with self.assertRaises(ValueError):
            get_kld_scape(ps_wrong_type)

        ps_wrong_pc = np.ones((10, 10, 11))
        with self.assertRaises(ValueError):
            get_kld_scape(ps_wrong_pc)

        ps_neg_value = np.ones((10, 10, 12))

        ps_neg_value[0, 0, 3] = -1  # add one negatif value

        with self.assertRaises(ValueError):
            get_kld_scape(ps_neg_value)

    def test_get_kld_scape_shape(self):
        piece = read_file(self.files[0], resolution=10)
        ps = get_pitch_scape(counts=piece)
        ret = get_kld_scape(ps)
        self.assertEqual(ret.shape, (10, 10))

    def test_get_kld_scape_correct_value(self):
        shape_piece = (10, 12)
        p1 = np.zeros(shape_piece)
        p1[0:5, 0] = 1  # all C
        p1[5:10, 2] = 1  # all D

        ps = get_pitch_scape(counts=p1)
        ret = get_kld_scape(ps)
        self.assertAlmostEqual(ret[0, 9], 0)
        self.assertAlmostEqual(ret[0, 4], np.log2(2))
        self.assertAlmostEqual(ret[0, 4], ret[5, 9])

    def test_reduce_scape_2d_input(self):
        with self.assertRaises(TypeError):
            reduce_scape_2d('scape')

        scape_wrong_size = np.ones((5, 6))
        with self.assertRaises(ValueError):
            reduce_scape_2d(scape_wrong_size)

        scape_wrong_dim = np.ones((5, 6, 9))
        with self.assertRaises(ValueError):
            reduce_scape_2d(scape_wrong_dim)

    def test_reduce_scape_2d_shape(self):
        counts = read_file_array(self.files, resolution=10)
        mi_scape = get_mi_scape(counts)
        mean, var = reduce_scape_2d(mi_scape)

        self.assertEqual(mean.shape, (2,))
        self.assertEqual(var.shape, (2, 2))

    def test_reduce_scape_2d_correct_value(self):
        shape_piece = (10, 12)
        p1 = np.zeros(shape_piece)
        p1[0:2, 0] = 1  # all C
        p1[8:10, 0] = 1  # all C

        p2 = np.zeros(shape_piece)
        p2[0:2, 2] = 1  # all D
        p2[8:10, 2] = 1  # all D

        p3 = np.zeros(shape_piece)
        p3[0:2, 4] = 1  # all E
        p3[8:10, 4] = 1  # all E

        p4 = np.zeros(shape_piece)
        p4[0:2, 7] = 1  # all G
        p4[8:10, 7] = 1  # all G

        corpus = np.vstack([p1[None], p2[None], p3[None], p4[None]])

        mi_scape = get_mi_scape(corpus)

        mi_mean_2d, mi_cov_2d = reduce_scape_2d(scape=mi_scape)

        self.assertAlmostEqual(mi_mean_2d[0], 4.5)
        self.assertAlmostEqual(mi_mean_2d[1], 17 / 3)

    def test_reduce_horizontale_inputs(self):
        with self.assertRaises(TypeError):
            reduce_scape_horizontale('scape')

        scape_wrong_size = np.ones((5, 6))
        with self.assertRaises(ValueError):
            reduce_scape_horizontale(scape_wrong_size)

        scape_wrong_dim = np.ones((5, 6, 9))
        with self.assertRaises(ValueError):
            reduce_scape_horizontale(scape_wrong_dim)

    def test_reduce_horizontale_shape(self):
        counts = read_file_array(self.files, resolution=10)
        mi_scape = get_mi_scape(counts)
        dist, var = reduce_scape_horizontale(mi_scape)

        self.assertEqual(dist.shape, (10,))
        self.assertEqual(var.shape, (10,))

    def test_reduce_horizontale_correct_value(self):
        shape_piece = (10, 12)
        p1 = np.zeros(shape_piece)
        p1[0:2, 0] = 1  # all C
        p1[8:10, 0] = 1  # all C

        p2 = np.zeros(shape_piece)
        p2[0:2, 2] = 1  # all D
        p2[8:10, 2] = 1  # all D

        p3 = np.zeros(shape_piece)
        p3[0:2, 4] = 1  # all E
        p3[8:10, 4] = 1  # all E

        p4 = np.zeros(shape_piece)
        p4[0:2, 7] = 1  # all G
        p4[8:10, 7] = 1  # all G

        corpus = np.vstack([p1[None], p2[None], p3[None], p4[None]])

        mi_scape = get_mi_scape(corpus)

        dist, var = reduce_scape_horizontale(mi_scape)

        self.assertEqual(dist[0], 0)
        self.assertAlmostEqual(dist[1], 4 / 9)
        self.assertEqual(dist[8], 2)
        self.assertEqual(dist[9], 2)

    def test_reduce_1d_input(self):
        with self.assertRaises(TypeError):
            reduce_1d('arr')

        arr_wrong_size = np.ones((5, 6))
        with self.assertRaises(ValueError):
            reduce_1d(arr_wrong_size)

    def test_reduce_horizontale_shape(self):
        counts = read_file_array(self.files, resolution=10)
        mi_scape = get_mi_scape(counts)
        dist, var = reduce_scape_horizontale(mi_scape)
        cog, var_1d = reduce_1d(dist)

        self.assertEqual(type(cog), np.float64)
        self.assertEqual(type(var_1d), np.float64)

    def test_reduce_correct_input(self):
        shape_piece = (10, 12)
        p1 = np.zeros(shape_piece)
        p1[0:2, 0] = 1  # all C
        p1[8:10, 0] = 1  # all C

        p2 = np.zeros(shape_piece)
        p2[0:2, 2] = 1  # all D
        p2[8:10, 2] = 1  # all D

        p3 = np.zeros(shape_piece)
        p3[0:2, 4] = 1  # all E
        p3[8:10, 4] = 1  # all E

        p4 = np.zeros(shape_piece)
        p4[0:2, 7] = 1  # all G
        p4[8:10, 7] = 1  # all G

        corpus = np.vstack([p1[None], p2[None], p3[None], p4[None]])

        mi_scape = get_mi_scape(corpus)

        dist, var = reduce_scape_horizontale(mi_scape)

        cog, var_1d = reduce_1d(dist)

        self.assertAlmostEqual(cog, 352 / 46)

    def test_bootstrap_type(self):
        func = lambda x: x

        with self.assertRaises(TypeError):
            bootstrap('data', func, n=10)

        with self.assertRaises(ValueError):
            bootstrap(self.file_simple_example, func, n=-10)

        with self.assertRaises(ValueError):
            bootstrap(data=np.asarray(self.file_simple_example), n=10)

    def test_bootstrap_output(self):
        res = bootstrap(np.asarray(self.file_simple_example), lambda x: x, 10)
        self.assertTrue(type(res) == list or type(res) == np.ndarray )
        self.assertEqual(len(res), 10)


if __name__ == '__main__':
    print(unittest.main())
