from flask import Flask, request, jsonify, Blueprint
from flaskext.mysql import MySQL
from src.sql import *
manageShareholder = Blueprint('manageShareholder', __name__)

@manageShareholder.route("/getAllShareholder/<term>/<year>",methods=['get'])
def getAllShareholder(term,year):
    data = request.json

    conn = mysql.connect()
    cursor = conn.cursor()

    query = "SELECT * FROM `shareholder%s/%s` WHERE 1"%(term,year)
    cursor.execute(query)
    data = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    jsonResult = toJson(data,columns)

    # return jsonify(jsonResult)


    for index,obj in enumerate(jsonResult):
        jsonResult[index]['text'] = "%s %s %s %s"%(jsonResult[index]['firstname'],jsonResult[index]['lastname'],jsonResult[index]['companyname'],jsonResult[index]['memberid'])
    # jsonResult['status'] = "success"
        # result['data'] = jsonResult
    # except:
    #     jsonResult = { "status" : "fail", "message" : "Error sql excute" }

    cursor.close()
    return jsonify(jsonResult)
