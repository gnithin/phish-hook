import pickle
from features import get_features_for_url
from abstract_classifier import AbstractClassifier
import numpy as np


class GregaClassifier(AbstractClassifier):
    def __init__(self, modelPath):
        with open(modelPath, "rb") as f:
            self.clf = pickle.load(f)

    def predict(self, url) -> bool:
        features = get_features_for_url(url)
        feature_input = np.array(features).reshape(1, -1)
        res = self.clf.predict(feature_input)
        if res[0] == 1:
            return True
        return False