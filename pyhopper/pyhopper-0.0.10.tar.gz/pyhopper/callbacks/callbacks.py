class Callback:
    def on_evaluate_start(self, candidate):
        pass

    def on_evaluate_end(self, candidate, f):
        pass

    def on_evaluate_cancelled(self, candidate):
        pass

    def on_new_best(self, new_best, f):
        pass

    def on_search_start(self):
        pass

    def on_search_end(self, best, best_f, history):
        pass