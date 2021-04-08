import tensorflow as tf
from keras_tweaks import dense_sparse_matmul


class Test_dense_sparse_matmul(tf.test.TestCase):
    def test1(self):
        h = tf.constant([1., 2., 3.])
        W = tf.sparse.SparseTensor(
            indices=([0, 1], [1, 1], [1, 2], [2, 0], [2, 2]),
            values=[1., 2., 3., 4., 5.],
            dense_shape=(3, 3))
        net = dense_sparse_matmul(h, W)
        self.assertAllEqual(net, [[12., 5., 21.]])


if __name__ == "__main__":
    tf.test.main()
