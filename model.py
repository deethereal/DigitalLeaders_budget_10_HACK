import numpy as np

class RegressionModel(object):
    def __init__(self):
        self.model = None # load model


    def predict(self, data):
        return np.random.randint(0, 100, data.shape[0])











