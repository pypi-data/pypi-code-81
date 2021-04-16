import os
import csv


from tensorflow.python.keras.models import load_model

from graphmanagerlib.DataForGCN import DataTransformer
from graphmanagerlib.Node import Node

import stellargraph as sg
from stellargraph import StellarGraph
from stellargraph.mapper import FullBatchNodeGenerator, pd
from stellargraph.layer import GCN

from tensorflow.keras import layers, optimizers, losses, Model
from sklearn import preprocessing, model_selection

from tensorflow.python.keras.callbacks import EarlyStopping



class GraphManager :
    def __init__(self, documents, tagsPath):
        tags = []
        with open(tagsPath, newline='') as inputfile:
            for row in csv.reader(inputfile):
                tags.append(row[0])
        self.nodes, self.edges, self.tags = DataTransformer().get_data(documents=documents,
                                                                       tags=tags)

    def TrainModel(self):
        nodes = self.nodes
        nodes.reset_index(inplace=True)
        node_subjects = nodes['tag']

        train_subjects, test_subjects = model_selection.train_test_split(
            node_subjects, train_size=0.8, test_size=None, stratify=node_subjects
        )
        val_subjects, test_subjects = model_selection.train_test_split(
            test_subjects, train_size=0.2, test_size=None, stratify=test_subjects
        )

        target_encoding = preprocessing.LabelBinarizer()

        train_targets = target_encoding.fit_transform(train_subjects)
        val_targets = target_encoding.transform(val_subjects)
        test_targets = target_encoding.transform(test_subjects)

        i = 0
        for tag in self.tags:
            nodes['tag'] = nodes['tag'].replace(tag, i)
            i += 1

        G = StellarGraph(nodes, self.edges)
        generator = FullBatchNodeGenerator(G, method="gcn")

        train_gen = generator.flow(train_subjects.index, train_targets)

        gcn = GCN(
            layer_sizes=[16, 16], activations=["relu", "relu"], generator=generator, dropout=0.5
        )

        x_inp, x_out = gcn.in_out_tensors()

        x_out

        predictions = layers.Dense(units=train_targets.shape[1], activation="softmax")(x_out)

        model = Model(inputs=x_inp, outputs=predictions)
        model.compile(
            optimizer=optimizers.Adam(lr=0.01),
            loss=losses.categorical_crossentropy,
            metrics=["acc"],
        )

        val_gen = generator.flow(val_subjects.index, val_targets)

        es_callback = EarlyStopping(monitor="val_acc", patience=50, restore_best_weights=True)


        history = model.fit(
            train_gen,
            epochs=200,
            validation_data=val_gen,
            verbose=2,
            shuffle=False,  # this should be False, since shuffling data means shuffling the whole graph
            callbacks=[es_callback],
        )

        sg.utils.plot_history(history)

        test_gen = generator.flow(test_subjects.index, test_targets)

        test_metrics = model.evaluate(test_gen)

        print(f'\nTest Set Metrics:', flush=True)

        for name, val in zip(model.metrics_names, test_metrics):
            print("\t{}: {:0.4f}".format(name, val), flush=True)

        root_dir = os.path.dirname(os.path.abspath(__file__));
        model_Path = root_dir + "\Model"
        model.save(model_Path)


        print ("===== Modèle entrainé et sauvegardé =====")


def singlePrediction(modelPath,document):
    reconstructed_model = load_model(modelPath)

    documentNodes = document[0].nodes
    inputSize = reconstructed_model.input_shape[0][1]
    while len(documentNodes) < inputSize:
        documentNodes.append(Node(XMin=-1, YMin=-1, XMax=-1, YMax=-1, Tag='null'))

    nodes, edges, tags = DataTransformer().get_data(document, tags=pd.DataFrame(['undefined']))
    nodes.reset_index(inplace=True)
    nodesSubject = nodes['tag']

    nodes['tag'] = nodes['tag'].replace('undefined', 0)

    G = StellarGraph(nodes, edges)
    generator = FullBatchNodeGenerator(G, method="gcn")

    target_encoding = preprocessing.LabelBinarizer()
    targets = target_encoding.fit_transform(nodesSubject)
    all_gen = generator.flow(nodesSubject.index, targets)

    ##TRANSPOSE ?
    # check model generalisation on the test set
    (loss, accuracy) = reconstructed_model.evaluate(all_gen)
    print(f"Test set: loss = {loss}, accuracy = {accuracy}")

    all_predictions = reconstructed_model.predict(all_gen)

    node_predictions = target_encoding.inverse_transform(all_predictions.squeeze())

    df = pd.DataFrame({"Predicted": node_predictions, "True": nodesSubject})
    df.head(20)
    print(df.to_string())



