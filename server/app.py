from flask import Flask, request, jsonify
from urllib.parse import urlparse
from features import get_features_for_url
from grega_classifier import GregaClassifier

import pickle
import numpy as np

from uci import Phishing

app = Flask(__name__)

classifiers = []


@app.route("/detect", methods=["POST"])
def detect():
    url = request.form["url"]
    resp = {
        "success": True,
        "message": "",
        "is_phishing": False,
        "payload": "",
    }

    if not url:
        resp["success"] = False
        resp["message"] = "url data-field is missing!"
    else:
        resp["success"] = True
        resp["is_phishing"] = is_phishing(url)
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
        return is_mal_count > 0:

    # TODO: Return unsure result
    return False


def setup_models():
    global classifiers

    grega_clf = GregaClassifier("./model.pkl")
    classifiers.append(grega_clf)

    uci_clf = Phishing("models/decision-uci.joblib")
    classifiers.append(uci_clf)


if __name__ == "__main__":
    print("Loading the models!")
    setup_models()

    print("Running the server")
    app.run(host="0.0.0.0", port=9999)