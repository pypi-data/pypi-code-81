import os
from dataclasses import dataclass
from typing import Tuple, TypeVar

from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.layers import Dense, Dropout, Input
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam

basic_layer = TypeVar("basic_layer")


@dataclass
class SimpleModel:
    """
    class containing default parameter of the
    Keras model
    """

    n_layers: int = 2
    input_size: Tuple = (1024,)
    n_neurons: int = 128
    dropout_rate: int = 0.1
    lr: float = 0.001
    batch_size: int = 32
    output_neurons: int = 1
    output_activation: str = "sigmoid"
    save_dir: str = "checkpoint"
    batch_size: int = 32
    epochs: int = 30


class SimpleModelKeras(SimpleModel):
    """
    Class for a basic keras model
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = None

    def build_model(self, **kwargs) -> Model:
        input_ = Input(self.input_size)
        x_layer = input_
        for _ in range(self.n_layers):
            x_layer = self._basic_layer(x_layer)

        x_layer = Dense(self.output_neurons,
                        activation=self.output_activation)(x_layer)
        output = Model(input_, x_layer)

        self.model = output

    def _basic_layer(self, x_layer: basic_layer, **kwargs):
        """Basic interface for keras model"""
        x_layer = Dense(self.n_neurons, activation="relu")(x_layer)
        x_layer = Dropout(self.dropout_rate)(x_layer)

        return x_layer

    def compile(self, **kwargs):
        """Basic interface for model compile"""
        opt = Adam(self.lr)
        output_activation = self.output_activation
        loss = (
            "binary_crossentropy"
            if output_activation == "sigmoid"
            else "categorical_crossentropy"
        )
        self.model.compile(optimizer=opt, loss=loss, metrics=["acc"])

    def fit(self, X, y, **kwargs):
        assert (
            self.model._is_compiled and (self.model is not None),
            "You must build and complile the model first",
        )
        ckpt = ModelCheckpoint(
            os.path.join(self.save_dir, "model.h5"),
            monitor="val_acc",
            mode="max",
            verbose=True,
            save_best_only=True,
        )
        earlystopping = EarlyStopping(
            monitor="val_acc", min_delta=0.0001, patience=5, mode="max", verbose=True
        )
        self.model.fit(
            X,
            y,
            epochs=self.epochs,
            batch_size=self.batch_size,
            validation_split=0.2,
            callbacks=[ckpt, earlystopping],
            **kwargs
        )


class AutoModelKeras(SimpleModelKeras):
    def __init__(self, **kwargs):
        super().__init__()
        self.build_model(**kwargs)
        self.compile(**kwargs)
