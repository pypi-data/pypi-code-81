import unittest

import ingest_data
import score
import train


class TestMLE(unittest.TestCase):
    def test_readcheck(self):
        self.assertIsNotNone(ingest_data.strat_train_set.shape, msg = "Check Done")
        self.assertIsNotNone(ingest_data.strat_test_set.shape, msg = "Check Done")
    def test_train(self):
        self.assertIsNotNone(train.lin_reg.intercept_)
    def test_score(self):
        self.assertIsNotNone(score.housing_predictions.shape)

if __name__ == '__main__':
   unittest.main()
