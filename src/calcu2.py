#!/usr/bin/env python
# -*- coding: utf-8 -*-
from src.sql import *

@app.route("/calculateTheScore/<term>/<year>",methods=['post'])
def calculateTheScore(term,year):
    # term,year,uuid,createby
    data = request.json
    conn = mysql.connect()
    cursor = conn.cursor()
    uuid = data['uuid']

    # get memberid  and q_share of all shareholders
    query = "SELECT `shareholder%s/%s`.`memberid`, `shareholder%s/%s`.`q_share` FROM `shareholder%s/%s` WHERE 1"%(term,year,term,year,term,year)
    cursor.execute(query)
    result = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    jsonResult = toJson(result,columns)
    shareholder = {}
    for obj  in jsonResult:
        shareholder['%s'%(obj['memberid'])] = obj['q_share']

    # get all code that allrady scan in our system
    query2 = "SELECT * FROM `qrcodescan%s/%s` WHERE `agenda_uuid` LIKE '%s' AND valid = 1  "%(term,year,uuid)
    cursor.execute(query2)
    result = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    jsonResult = toJson(result,columns)

    accept = 0
    noaccept = 0
    abstain = 0
    broke = 0
    createby = "manassanan.bo"
    # createby = data['createby']


    for obj in jsonResult:
        q_share = shareholder[''+obj['memberid']]
        answer = obj['answer']
        if answer is 1:
            accept += q_share
        elif answer is 2:
            noaccept += q_share
        elif answer is 3:
            abstain += q_share
        elif answer is 2:
            broke += q_share

    # check this agenda is alredy summit score
    query3 = "SELECT * FROM `submit` WHERE `agenda_uuid` LIKE '%s' "%(uuid)
    cursor.execute(query3)
    result = cursor.fetchone()
    if result is not None:
        query4 = "UPDATE `submit` SET valid = 0 WHERE `agenda_uuid` LIKE '%s'"%(uuid)
        cursor.execute(query4)

    query5 = "INSERT INTO `submit`(`agenda_uuid`, `term`, `year`, `accept`, `noaccept`, `abstain`, `broke`, `createby`, `createat`, `valid`) VALUES ('%s',%s,%s,%s,%s,%s,%s,'%s',CURRENT_TIME,1)"%(uuid,term,year,accept,noaccept,abstain,broke,createby)
    cursor.execute(query5)
    conn.commit()

    return jsonify(jsonResult)
