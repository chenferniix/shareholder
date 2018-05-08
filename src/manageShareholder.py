from flask import Flask, request, jsonify, Blueprint
from flaskext.mysql import MySQL
manageShareholder = Blueprint('manageShareholder', __name__)

@manageShareholder.route("/getAllShareholder/<term>/<year>",methods=['get'])
def getAllShareholder(term,year):
    data = request.json
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        query = "SELECT * FROM shareholder%s/%s WHERE 1"%(term,year)
        cursor.execute(query)
        jsonResult = [{columns[index][0]:column for index, column in enumerate(value)}   for value in cursor.fetchall()]
        for obj in jsonResult:
            jsonResult['text'] = "%s %s %s %s"%(jsonResult['firstname'],jsonResult['lastname'],jsonResult['companyname'],jsonResult['memberid'])
            jsonResult['status'] = "success"
    except:
        jsonResult = { "status" : "fail", "message" : "Error sql excute" }

    cursor.close()
    return jsonify(jsonResult)
