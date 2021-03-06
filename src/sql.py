#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify, Blueprint
from flaskext.mysql import MySQL
sql = Blueprint('sql', __name__)
mysql = MySQL()
# app.config['MYSQL_DATABASE_USER'] = 'root'
# app.config['MYSQL_DATABASE_PASSWORD'] = '^dglnvg8hkw,j0y[,nv-'
# app.config['MYSQL_DATABASE_DB'] = 'smp'
# app.config['MYSQL_DATABASE_HOST'] = '203.150.57.159'

app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'devops@Pass01'
app.config['MYSQL_DATABASE_DB'] = 'shareholder_meeting'
app.config['MYSQL_DATABASE_HOST'] = '203.154.58.87'
mysql.init_app(app)

def toJson(data,columns):
    results = []
    for row in data:
        results.append(dict(zip(columns, row)))
    return results

def fetchOnetoJson(data,columns):
    result =  dict(zip(columns, data))
    return result
