# coding=utf-8
import os
# multi-gpu ids
os.environ["CUDA_VISIBLE_DEVICES"] = "4"
import tf_geometric as tfg
from tf_geometric.layers import GCN
from tensorflow.keras.regularizers import L1L2
import tensorflow as tf


graph, (train_index, valid_index, test_index) = tfg.datasets.CoraDataset().load_data()
num_classes = graph.y.max() + 1
learning_rate = 1e-2
l2_coef = 5e-4

model = tfg.layers.GAT(units=5)
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-1),
    loss=tf.keras.losses.categorical_crossentropy
)

print(model([graph.x, graph.edge_index]))