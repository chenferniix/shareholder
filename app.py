from flask import Flask, request, jsonify, session,current_app
from flaskext.mysql import MySQL
from json import dumps
from json import loads
import json
# import requests
# from flask_cors import CORS, cross_origin
import os



MYDIR = os.path.dirname(__file__)
# app = Flask(__name__)

from src.sql import *
from src.calculateScore import *
from src.calcu2 import *
from src.manageAgenda import *
from src.manageShareholder import *
from src.QRServer import *

# CORS(app)


@app.route("/login",methods=['POST'])
def login():
    data = request.json
    conn = mysql.connect()
    cursor = conn.cursor()
    query = "SELECT * FROM admin INNER JOIN role on admin.role = role.roleid WHERE username LIKE '"+data['username']+"' AND password LIKE '"+data['password']+"' AND valid = 1  "
    cursor.execute(query)
    result = cursor.fetchone()
    if result is not None:
        columns = cursor.description
        jsonResult = {columns[index][0]:column for index, column in enumerate(result)}
        # jsonResult = [{columns[index][0]:column for index, column in enumerate(value)}   for value in cursor.fetchall()]
        obj = { "status" : "success", "info" :  jsonResult }
        return jsonify(obj)
    else:
        obj = { "status" : "fail" }
        return jsonify(obj)
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
