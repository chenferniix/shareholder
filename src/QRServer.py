#!/usr/bin/env python
# -*- coding: utf-8 -*-
from src.sql import *

@app.route("/vote",methods=['post'])
def vote():
    data = request.json
    conn = mysql.connect()
    cursor = conn.cursor()
    # try:

    termYear = "%s/%s"%(data['term'],data['year'])
    # term,year,uuid,memberid,createby,answer
    # ---------check memberid and register--------
    queryMember = "SELECT * FROM `shareholder%s` WHERE `memberid` LIKE '%s' AND `register` =1 "%(termYear,data['memberid'])
    cursor.execute(queryMember)
    result = cursor.fetchone()
    returnJson = {}
    if result is not None:
        query = "SELECT * FROM `qrcodescan%s` WHERE `memberid` LIKE '%s' AND `agenda_uuid` LIKE '%s' AND valid = 1 "%(termYear,data['memberid'],data['uuid'])
        cursor.execute(query)
        result = cursor.fetchone()
        # -----------check already vote-------------
        if result is not None:
            query2 = "UPDATE `qrcodescan%s` SET `valid` = '0' WHERE `qrcodescan%s`.`agenda_uuid` LIKE '%s' AND `qrcodescan%s`.`memberid` LIKE '%s'"%(termYear,termYear,data['uuid'],termYear,data['memberid'])
            cursor.execute(query2)
        # ------------insert vote----------------
        query3 = "INSERT INTO `qrcodescan%s` (`id`, `agenda_uuid`, `memberid`, `answer`, `createby`, `createat`, `valid`) VALUES (NULL, '%s', '%s', %s, '%s', CURRENT_TIMESTAMP, '1')"%(termYear,data['uuid'],data['memberid'],data['answer'],data['createby'])
        # return query3
        cursor.execute(query3)
        conn.commit()
        returnJson = {"status": "success", "info": data}
    else:
        returnJson = {"status": "fail", "info": data ,"message": "Not found `memberid`: "+data['memberid']}
    cursor.close()
    return jsonify(returnJson)
    # except:
    #     returnJson = {"status": "error", "info": data , "message": "Error post data or database incorrect."}
    #     return jsonify(returnJson)




@app.route("/checkQRCode",methods=['post'])
def checkQRCode():
    data = request.json
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        # term,year,uuid,memberid
        termYear = "%s/%s"%(data['term'],data['year'])
        query = "SELECT * FROM `qrcodescan%s` JOIN  `shareholder%s` ON `shareholder%s`.`memberid` = `qrcodescan%s`.`memberid` WHERE `qrcodescan%s`.`memberid` LIKE '%s' AND `qrcodescan%s`.`agenda_uuid` LIKE '%s' AND valid = 1 "%(termYear,termYear,termYear,termYear,termYear,data['memberid'],termYear,data['uuid'])
        cursor.execute(query)
        result = cursor.fetchone()
        returnJson = {}

        if result is not None:
            columns = [column[0] for column in cursor.description]
            jsonResult = fetchOnetoJson(result,columns)
            returnJson = {"status": 'found', "info": jsonResult}


        else:
            returnJson = {"status": 'not found'}
        cursor.close()
        return jsonify(returnJson)
    except:
        cursor.close()
        return jsonify({"status": "error", "info": data , "message": "Error post data or database incorrect."})
