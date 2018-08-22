#!/usr/bin/env python
# -*- coding: utf-8 -*-
from src.sql import *
import uuid

@app.route("/getAgendaInYear/<term>/<year>",methods=['get'])
def getAgendaInYear(term,year):
    data = request.json
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        query = "SELECT * FROM agenda WHERE term = %s AND year = %s AND valid = 1"%(term,year)
        cursor.execute(query)
        data = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        jsonResult = toJson(data,columns)

    except:
        jsonResult = { "status" : "fail", "message" : "Error sql excute" }

    cursor.close()
    return jsonify(jsonResult)


@app.route("/addAgenda",methods=['POST'])
def addAgenda():
    # uuid,agenda,subagenda,title,short_title,imagepath,term,year,createby
    data = request.json
    conn = mysql.connect()
    cursor = conn.cursor()

    # uuid = ""
    uid = str(uuid.uuid4())[0:7]
    # uuid = uuid.uuid4()[0:7]
    # return uid
    # try:
    query = "INSERT INTO agenda (uuid,agenda,subagenda,title,short_title,imagepath,term,year,createby) VALUES  ('%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(uid, data['agenda'], data['subagenda'], data['title'], data['short_title'], data['imagepath'], data['term'], data['year'], data['username'])
    # return query

    cursor.execute(query)
    conn.commit()
    data['uuid'] = uid
    obj = { "status" : "success", "data" :  data }
    # except:
        # obj = { "status" : "fail", "data" :  data , "message": "Insert Error"}

    return jsonify(obj)

    cursor.close()


@app.route("/editAgenda",methods=['POST'])
def editAgenda():
    #  uuid,agenda,subagenda,title,short_title,imagepath,term,year,createby
    data = request.json
    conn = mysql.connect()
    cursor = conn.cursor()

    # ------ check uuid is exist ----------------
    try:
        query = "SELECT * FROM agenda WHERE uuid LIKE '%s' AND valid = 1 ORDER BY id DESC"%(data['uuid'])
        cursor.execute(query)
        result = cursor.fetchone()
        if result is None:

            # jsonResult = [{columns[index][0]:column for index, column in enumerate(value)}   for value in cursor.fetchall()]
            obj = { "status" : "fail", "message" : "Dont have uuid : %s in agenda table "%(uuid) }
            cursor.close()
            return jsonify(obj)
    except:
        obj = { "status" : "fail", "message" : "Dont have uuid in data" }
        cursor.close()
        return jsonify(obj)

    # --------- insert new row and set old to invalid ---------------
    try:

        query = "UPDATE agenda SET valid = 0 WHERE uuid LIKE %s"%(data['uuid'])
        cursor.execute(query)

        query2 = "INSERT INTO agenda (uuid,agenda,subagenda,title,short_title,imagepath,term,year,createby) VALUES '%s','%s','%s','%s','%s','%s','%s','%s',"%(data['uuid'], data['agenda'], data['subagenda'], data['title'], data['short_title'], data['imagepath'], data['term'], data['year'], data['createby'])
        cursor.execute(query2)

        conn.commit()
        obj = { "status" : "success", "data" :  data }
    except:
        obj = { "status" : "fail", "data" :  data }

    cursor.close()
    return jsonify(obj)


@app.route("/removeAgenda",methods=['POST'])
def removeAgenda():
    # uuid
    data = request.json
    conn = mysql.connect()
    cursor = conn.cursor()

    # ------ check uuid is exist ----------------
    try:
        query = "SELECT * FROM agenda WHERE uuid LIKE '%s' AND valid = 1 ORDER BY id DESC"%(data['uuid'])
        cursor.execute(query)
        result = cursor.fetchone()
        if result is None:

            #jsonResult = [{columns[index][0]:column for index, column in enumerate(value)}   for value in cursor.fetchall()]
            obj = { "status" : "fail", "message" : "Dont have uuid : %s in agenda table "%(uuid) }
            cursor.close()
            return jsonify(obj)
        else:
            jsonResult = {columns[index][0]:column for index, column in enumerate(cursor.fetchone())}
            try:

                query = "UPDATE `agenda` SET valid = 0 WHERE uuid LIKE %s"%(data['uuid'])
                cursor.execute(query)
                conn.commit()
                obj = { "status":"remove success", "data": jsonResult }

            except:
                obj = { "status":"remove fail", "data": jsonResult }


    except:
        obj = { "status" : "fail", "message" : "Dont have uuid in data" }

    cursor.close()
    return jsonify(obj)


@app.route("/getTermYear",methods=['POST'])
def getTermYear():
    conn = mysql.connect()
    cursor = conn.cursor()
    query = "SELECT  * FROM meeting WHERE valid = 1"
    cursor.execute(query)
    result = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    jsonResult = toJson(result,columns)
    # arr = []
    # for obj in result:
    #     arr.append(obj[0])
    # for index,obj in enumerate(jsonResult):
    #     jsonResult[index]['text'] = "%s"%(jsonResult[index]['year'])
    cursor.close()
    return jsonify(jsonResult)


# @app.route("/removeAgenda",methods=['POST'])
# def removeAgenda():
