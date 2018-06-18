#!/usr/bin/env python
# -*- coding: utf-8 -*-
from src.sql import *

@app.route("/getAgendaInYear/<year>",methods=['get'])
def getAgendaInYear(year):
    data = request.json
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        query = "SELECT * FROM agenda WHERE year = %s AND valid = 1"%(year)
        cursor.execute(query)
        jsonResult = [{columns[index][0]:column for index, column in enumerate(value)}   for value in cursor.fetchall()]

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
    uuid = uuid.uuid4()[0:7]
    try:
        query = "INSERT INTO agenda (uuid,agenda,subagenda,title,short_title,imagepath,term,year,createby) VALUES '%s','%s','%s','%s','%s','%s','%s','%s',"%(uuid, data['agenda'], data['subagenda'], data['title'], data['short_title'], data['imagepath'], data['term'], data['year'], data['createby'])

        cursor.execute(query)
        conn.commit()
        data['uuid'] = uuid
        obj = { "status" : "success", "data" :  data }
    except:
        obj = { "status" : "fail", "data" :  data , "message": "Insert Error"}
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


# @app.route("/removeAgenda",methods=['POST'])
# def removeAgenda():
