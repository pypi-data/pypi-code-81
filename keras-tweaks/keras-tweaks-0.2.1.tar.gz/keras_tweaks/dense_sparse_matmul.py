import tensorflow as tf


def dense_sparse_matmul(denV: tf.Tensor, spW: tf.SparseTensor) -> tf.Tensor:
    """Multiply row vector with sparse matrix

    Parameters:
        denV (tf.Tensor): Dense 1xN row vector.
        spW (tf.SparseTensor): Sparse NxM matrix.

    Returns:
        tf.Tensor: Dense 1xM row vector

    Motivation:
        TF only supports multiplying a sparse matrix with a column vector.
        By transposing, we can use `tf.sparse.sparse_dense_matmul` to
        multiply a row vector with a sparse matrix. The later multiplication
        is commonly used in context of neural networks in TF/Keras.
    """
    # reshape to list of row vectors if neccessary
    if denV.shape.ndims == 1:
        denV = tf.reshape(denV, (1, -1))
    # transpose -> multiply -> transpose back
    return tf.transpose(tf.sparse.sparse_dense_matmul(
        tf.sparse.transpose(spW), tf.transpose(denV)))
