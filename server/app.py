from flask import Flask, request, jsonify
from urllib.parse import urlparse
from grega_classifier import GregaClassifier
import pickle
import numpy as np
from uci import Phishing
from whitelist import Whitelist
from joblib import Parallel, delayed
import functools
import sys


app = Flask(__name__)
classifiers = []
whitelist = Whitelist()

UCI_MODEL_PATH = "./models/uci/decision-uci.joblib"
GREGA_MODEL_PATH = "./models/grega/small-ensemble-knn-rf-dt.pkl"
WHITELIST_CSV_PATH = "./data/whitelist_domains.csv"


def is_valid_url_scheme(url):
    """ Determine if the url has valid scheme for phishing-detection """
    if url is None or len(url.strip()) == 0:
        return False
    parsed_url = urlparse(url)
    scheme = parsed_url.scheme
    return scheme in ("http", "https")


@app.route("/detect", methods=["POST"])
def detect():
    """ Endpoint to detect if the given url is a phishing url """
    url = request.form["url"]
    resp = {
        "success": True,
        "message": "",
        "consensus_reached": True,
        "is_phishing": False,
        "payload": "",
    }

    print(f"URL - {url}")

    if not is_valid_url_scheme(url):
        resp["success"] = False
        resp["message"] = "Invalid url"

    # check if url is whitelisted
    elif whitelist.contains_url(url):
        print(f"Whitelisted domain - {url}")

        resp["success"] = True
        resp["is_phishing"] = False
        resp["consensus_reached"] = True
        resp["payload"] = url
        resp["message"] = "Whitelisted Url"

    else:
        resp["success"] = True
        phishing_result, consensus_reached = is_phishing(url)
        resp["is_phishing"] = phishing_result
        resp["consensus_reached"] = consensus_reached
        resp["payload"] = url

    return jsonify(resp)


@functools.cache
def is_phishing(url):
    """ Given a url, is_phishing returns True if it's a phishing url, False otherwise """
    global classifiers
    is_mal_count = 0
    is_not_mal_count = 0

    def run_predict(c, url):
        return c.predict(url)

    # Predict in parallel
    result = Parallel(n_jobs=len(classifiers))(
        delayed(run_predict)(clf, url) for clf in classifiers
    )

    for r in classifiers:
        if r:
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
    """ Initialize all the models """
    global classifiers

    grega_clf = GregaClassifier(GREGA_MODEL_PATH)
    classifiers.append(grega_clf)

    uci_clf = Phishing(UCI_MODEL_PATH)
    classifiers.append(uci_clf)


def setup_whitelist():
    """ Fetch the whitelist externally and load it in the program """
    global whitelist
    whitelist.load(WHITELIST_CSV_PATH)


if __name__ == "__main__":
    # Optional args to get the host and port
    host = "0.0.0.0"
    port = 9999

    if len(sys.argv) > 1:
        args = sys.argv[1:]
        host = args[0]
        if len(args) > 1:
            port = int(args[1])

    print("Setting up whitelist")
    setup_whitelist()

    print("Loading the models!")
    setup_models()

    print(f"Running the server on {host}:{port}")
    app.run(host=host, port=9999)