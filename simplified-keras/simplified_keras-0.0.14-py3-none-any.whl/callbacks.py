import io
import tensorflow.keras.callbacks as clb
from simplified_keras.metrics import get_confusion_matrixes
from simplified_keras.plots import plot_confusion_matrix
from simplified_keras.transformations import predictions_to_classes, one_hot_to_sparse
import tensorflow as tf
import matplotlib.pyplot as plt


def get_default_callbacks(model_path, monitor='val_acc', base_patience=3, lr_reduce_factor=0.5, min_lr=1e-7, verbose=1,
                          log_dir=None, gradients=True, confusion_matrix=True, loss=None, data=None, classes=None,
                          heatmap_options=None):
    callbacks = [
        clb.ReduceLROnPlateau(monitor=monitor, factor=lr_reduce_factor, min_lr=min_lr, patience=base_patience, verbose=verbose),
        clb.EarlyStopping(monitor=monitor, patience=(2 * base_patience + 1), verbose=verbose),
        clb.ModelCheckpoint(monitor=monitor, filepath=model_path, save_best_only=True, verbose=verbose)
    ]
    if log_dir:
        callbacks.append(ExtendedTensorBoard(log_dir, gradients, confusion_matrix, loss, data, classes, heatmap_options))

    return callbacks


def restore_callbacks(callbacks, best_monitor_value):
    for callback in callbacks:
        if isinstance(callback, (clb.ModelCheckpoint, clb.ReduceLROnPlateau)):
            if 'loss' in callback.monitor and best_monitor_value <= 0:
                raise ValueError(f'{callback.monitor} should be > 0')

            if 'acc' in callback.monitor and not 0 < best_monitor_value < 1:
                raise ValueError(f'{callback.monitor} should be between 0 and 1')
            callback.best = best_monitor_value


# TODO: Support generators
class ExtendedTensorBoard(clb.TensorBoard):
    def __init__(self, log_dir, gradients=True, confusion_matrix=True, loss=None, data=None, classes=None,
                 heatmap_options=None, **kwargs):
        super().__init__(log_dir=log_dir, **kwargs)
        self.loss = loss
        self.data = data
        self.classes = classes
        if not classes and data:
            self.classes = [i for i in range(len(data[1][0]))]
        self.heatmap_options = heatmap_options
        self.gradients = gradients
        self.confusion_matrix = confusion_matrix

    def on_epoch_end(self, epoch, logs=None):
        super().on_epoch_end(epoch, logs=logs)
        if self.gradients:
            assert self.loss and self.data, 'You have to pass loss and data arguments'
            self.__log_gradients(epoch)
        if self.confusion_matrix:
            assert self.data, 'You have to pass data argument'
            self.__log_confusion_matrix(epoch)
        self._train_writer.flush()

    def __log_gradients(self, epoch):
        x, y = self.data
        with tf.GradientTape(persistent=True) as tape:
            tape.watch(self.model.trainable_weights)
            z = self.model(x, training=True)
            loss = self.loss(y, z)
        grads = {w.name: tape.gradient(loss, w) for w in self.model.trainable_weights}

        with self._train_writer.as_default():
            for name, g in grads.items():
                mean = tf.reduce_mean(tf.abs(g))
                tf.summary.scalar(f"gradients_mean_{name}", mean, step=epoch)
                tf.summary.histogram(f"gradients_histogram_{name}", g, step=epoch)

    def __log_confusion_matrix(self, epoch):
        x, y = self.data
        test_pred = predictions_to_classes(self.model.predict(x))

        _, cm_normalized = get_confusion_matrixes(test_pred, one_hot_to_sparse(y))
        fig = plot_confusion_matrix(cm_normalized, self.classes, show=False)

        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight')
        plt.close(fig)
        buf.seek(0)
        image = tf.image.decode_png(buf.getvalue(), channels=4)
        image = tf.expand_dims(image, 0)

        with self._train_writer.as_default():
            tf.summary.image("Confusion Matrix", image, step=epoch)
