from multiprocessing import Manager


class TrainManager:
    def __init__(self):
        manager = Manager()
        self.train_status_mapping = manager.dict()

    def update(self, model_id, status):
        self.train_status_mapping[model_id] = status

    def check(self, model_id):
        if model_id in self.train_status_mapping:
            return self.train_status_mapping[model_id]
        return 'unknown'


train_manager = TrainManager()
