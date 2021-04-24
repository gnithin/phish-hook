import pickle
from features import get_features_for_url
from abstract_classifier import AbstractClassifier


class GregaClassifier(AbstractClassifier):
    def __new__(self, modelPath):
        with open("./model.pkl", "rb") as f:
            grega_clf = pickle.load(f)

    def predict(self, url) -> bool:
        features = get_features_for_url(url)
        feature_input = np.array(features).reshape(1, -1)
        res = clf.predict(feature_input)
        if res[0] == 1:
            return True
        return False