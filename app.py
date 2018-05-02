from flask import Flask, request, jsonify, Blueprint,render_template, session,current_app
from flaskext.mysql import MySQL
from json import dumps
from json import loads
import json
# import requests
from flask_cors import CORS, cross_origin
import os



MYDIR = os.path.dirname(__file__)
app = Flask(__name__)

from src.sql import *
from src.manageAgenda import *
from src.manageShareholder import *
from src.QRServer import *

CORS(app)
app.register_blueprint(sql)
app.register_blueprint(manageAgenda)
app.register_blueprint(manageShareholder)
app.register_blueprint(qrserver)


@app.route("/login",methods=['POST'])
def login():
    data = request.json
    conn = mysql.connect()
    cursor = conn.cursor()
    query = "SELECT * FROM admin WHERE username LIKE '"+data['username']+"' AND password LIKE '"+data['password']+"'"
    cursor.execute(query)
    result = cursor.fetchone()
    if result is not None:
        return "Login success" + str(result)
    else:
        return "Cannont login"
    cursor.close()

@app.route("/register",methods=['POST'])
def register():
    data = request.json
    conn = mysql.connect()
    cursor = conn.cursor()
    query = "SELECT * FROM register WHERE member_id = '1001' "
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return "Register success"
    else:
        return "Cannot Register"
    cursor.close()

@app.route("/hello",methods=['POST'])
def hello():
    current_app.logger.info("korkla")
    return "korkla"

if __name__ == "__main__":
    # socketio.run(app,debug=True,host='0.0.0.0',certfile='ssl/thaidotcom.cloud.cert',keyfile='ssl/*.thaidotcom.key')
    # socketio.run(app,debug=True,host='0.0.0.0')
    # app.run(host='0.0.0.0',port=5000, ssl_context=context, debug=True, threaded=True)
    app.run(host='0.0.0.0',port=5000,debug=True,threaded=True)
