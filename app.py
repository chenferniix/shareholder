from flask import Flask
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

@app.route("/")
def helloWorld():
  return "Hello, cross-origin-world!"


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True,threaded=True)
