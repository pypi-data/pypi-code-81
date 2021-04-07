import os
from torch.utils.data import Dataset
from multimodal import DEFAULT_DATA_DIR
from multimodal.utils import download_and_unzip
import json

class GQA(Dataset):

    url_questions = "https://nlp.stanford.edu/data/gqa/questions1.2.zip"
    url_scene_graphs = "https://nlp.stanford.edu/data/gqa/sceneGraphs.zip"

    def __init__(self, split="train", version="balanced", features=None, dir_data=None):
        """
        split: train, val, test, testdev, challenge
        version: balanced, all
        features: TODO
        dir_data: dir where multimodal files are downloaded. Default $APPLICATION_DATA/multimodal/
        """

        self.split = split
        self.version = version
        self.features = features

        if dir_data is None:
            dir_data = DEFAULT_DATA_DIR
        self.dir_dataset = os.path.join(dir_data, "datasets", "gqa")
        os.makedirs(self.dir_dataset, exist_ok=True)
        self.questions = []
        self.download()

        # load scene graphs
        print("Loading scene graphs")
        scene_graph_path = os.path.join(self.dir_dataset, f"{split}_sceneGraphs.json")
        if os.path.exists(scene_graph_path):
            with open(scene_graph_path) as f:
                self.scene_graphs = json.load(f)
        else:
            self.scene_graphs = None

        # load questions
        if self.version == "all" and self.split == "train":
            pass # TODO specific case
        else:
            question_path = os.path.join(self.dir_dataset, f"{split}_{version}_questions.json")
            with open(question_path) as f:
                self.questions = json.load(f)
            self.question_ids = list(self.questions.keys())

    def __len__(self) -> int:
        return len(self.questions)

    def __getitem__(self, index: int):
        qid = self.question_ids[index]
        return self.questions[qid]

    def download(self):
        print(f"Downloading questions from {self.url_questions} to {self.dir_dataset}.")
        # download_and_unzip(self.url_questions, self.dir_dataset)
        print(f"Downloading scene graphs from {self.url_scene_graphs} to {self.dir_dataset}.")
        # download_and_unzip(self.url_scene_graphs, self.dir_dataset)
