from flask import Flask, request, jsonify
from urllib.parse import urlparse
from features import get_features_for_url

app = Flask(__name__)

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
    # TODO: Add ML predict logic here
    features = get_features_for_url(url)
    res = clf.predict(features)[0]
    return res == 1

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999)
