from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/detect', methods=['POST'])
def detect():
    url = request.form['url']
    resp = {
            "success": True,
            "message": "",
            "is_malicious": False
            }
    if not url:
        resp["success"] = False
        resp["message"] = "url data-field is missing!"
    else:
        resp["success"] = True
        resp["is_malicious"] = is_malicious(url)
    
    return jsonify(resp)

def is_malicious(url):
    # TODO: Add ML predict logic here
    return url == "http://stackoverflow.com"


if __name__ == '__main__':
      app.run(host='0.0.0.0', port=9999)
