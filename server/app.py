from flask import Flask, request, jsonify
from urllib.parse import urlparse
from features import get_features_for_url
from grega_classifier import GregaClassifier
import pickle
import numpy as np
from uci import Phishing

app = Flask(__name__)
classifiers = []

UCI_MODEL_PATH = "./models/uci/decision-uci.joblib"
GREGA_MODEL_PATH = "./models/grega/ensemble-knn-rf-dt.pkl"


@app.route("/detect", methods=["POST"])
def detect():
    url = request.form["url"]
    resp = {
        "success": True,
        "message": "",
        "consensus_reached": True,
        "is_phishing": False,
        "payload": "",
    }

    if not url:
        resp["success"] = False
        resp["message"] = "url data-field is missing!"

    else:
        resp["success"] = True
        phishing_result, consensus_reached = is_phishing(url)
        resp["is_phishing"] = phishing_result
        resp["consensus_reached"] = consensus_reached
        resp["payload"] = url

    return jsonify(resp)


def is_phishing(url):
    global classifiers
    is_mal_count = 0
    is_not_mal_count = 0
    for c in classifiers:
        if c.predict(url):
            is_mal_count += 1
        else:
            is_not_mal_count += 1

    if is_mal_count == 0 or is_not_mal_count == 0:
        # we've got a definite result here
        return (is_mal_count > 0, True)

    # NOTE: Defaulting to phishing if unsure. A decision can be taken by the frontend about this info.
    # But in the future, if there many other entries, picking the majority should also work
    # Return unsure result
    return (True, False)


def setup_models():
    global classifiers

    grega_clf = GregaClassifier(GREGA_MODEL_PATH)
    classifiers.append(grega_clf)

    uci_clf = Phishing(UCI_MODEL_PATH)
    classifiers.append(uci_clf)


if __name__ == "__main__":
    print("Loading the models!")
    setup_models()

    print("Running the server")
    app.run(host="0.0.0.0", port=9999)