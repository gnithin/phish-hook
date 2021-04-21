from flask import Flask, request, jsonify
from urllib.parse import urlparse
from features import get_features_for_url

import pickle
import numpy as np

from uci import Phishing

app = Flask(__name__)

phishing = Phishing('models/decision-uci.joblib')
clf = None

@app.route('/detect', methods=['POST'])
def detect():
    url = request.form['url']
    resp = {
        "success": True,
        "message": "",
        "is_malicious": False,
        "payload": "",
    }
    if not url:
        resp["success"] = False
        resp["message"] = "url data-field is missing!"
    else:
        resp["success"] = True
        resp["is_malicious"] = is_malicious(url)
        resp["payload"] = url

    return jsonify(resp)


def is_malicious(url):
    # TODO: Incorporate this
    # return phishing.is_phishing(url)
    # Add ML predict logic here
    global clf
    print(f"Processing ${url}")
    print(clf)
    features = get_features_for_url(url)
    print(features)
    feature_input = np.array(features).reshape(1,-1)
    res = clf.predict(feature_input)
    print(res)
    if res[0] == 1:
        return True
    return False


def setup_model():
    global clf
    with open('./model.pkl', 'rb') as f:    # load
        clf = pickle.load(f)

if __name__ == '__main__':
    # build the model
    setup_model()
    print("Loaded the model!")
    print("Running the server")
    app.run(host='0.0.0.0', port=9999)
