#!/usr/bin/env python
# -*- coding: utf-8 -*-
from src.sql import *


@app.route("/getAllShareholder/<term>/<year>",methods=['get'])
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

    returnObj = []
    for index,obj in enumerate(jsonResult):
        text = ""
        if(jsonResult[index]['title'] != 'บริษัท'.decode('utf-8')):
            text = "%s %s %s"%(jsonResult[index]['firstname'],jsonResult[index]['lastname'],jsonResult[index]['memberid'])
        else:
            text = "%s %s"%(jsonResult[index]['companyname'],jsonResult[index]['memberid'])
        returnObj.append({'text': text, 'info': jsonResult[index] })
        # jsonResult[index]['text'] = "%s %s %s %s"%(jsonResult[index]['firstname'],jsonResult[index]['lastname'],jsonResult[index]['companyname'],jsonResult[index]['memberid'])

    # jsonResult['status'] = "success"
        # result['data'] = jsonResult
    # except:
    #     jsonResult = { "status" : "fail", "message" : "Error sql excute" }

    cursor.close()
    return jsonify(returnObj)



@app.route("/importShareholder",methods=['get'])
def importShareholder():
    df = pd.read_excel('shareholderFile/INET_XM_230418.xlsx', header=0)
    conn = mysql.connect()
    cursor = conn.cursor()
    query = "INSERT INTO `shareholder2/2018` (`id`, `memberid`, `q_share`, `title`, `firstname`, `lastname`, `companyname`, `ref`, `createat`, `regrister`, `registertime`, `proxytitle`, `proxyname`, `proxylastname`) VALUES "
    strQuery = ''
    # return str(df['Account_ID'].count())
    nRow = df['Account_ID'].count()
    listTitle = []
    for index,row in df.iterrows():
        if row['n_title'] == 'บริษัท'.decode('utf-8'):
            # return jsonify(row)
            # listTitle.append(row['n_title'])

            strQuery += "(%s, '%s', %s, '%s', NULL, NULL, '%s', '%s', CURRENT_TIMESTAMP, '0', NULL, NULL, NULL, NULL)"%(index+1,row['Account_ID'],row['q_share'],row['n_title'],row['n_last'],row['i_ref'])
        else:
            strQuery += "(%s, '%s', %s, '%s', '%s','%s',  NULL , '%s', CURRENT_TIMESTAMP, '0', NULL, NULL, NULL, NULL)"%(index+1,row['Account_ID'],row['q_share'],row['n_title'],row['n_first'],row['n_last'],row['i_ref'])

        if index+1 != nRow:
            strQuery += ","
        # else:
        #     strQuery += ";"
    # return str(listTitle)
    # return "eiei"
    # return query+strQuery
    cursor.execute(query+strQuery)
    conn.commit()

    data = {"status": "success"}
    cursor.close()
    return jsonify(data)


@app.route("/register/<term>/<year>",methods=['post'])
def register(term,year):
    conn = mysql.connect()
    cursor = conn.cursor()
    data = request.json
    query = 'SELECT * FROM `shareholder%s/%s` WHERE `memberid` = %s'%(term,year,data['memberid'])
    cursor.execute(query)
    result = cursor.fetchone()
    returnData = {}
    if result is not None:
        # columns = [column[0] for column in cursor.description]
        # jsonResult = fetchOnetoJson(result,columns)
        jsonResult = {}
        try:
            query2 = ''
            if data['registertype'] == 'proxy':
                query2 = "UPDATE `shareholder%s/%s` SET `register` = '1', `registerby`= '%s', `registertime` = CURRENT_TIMESTAMP, `proxytitle` = '%s', `proxyname`= '%s', `proxylastname` = '%s' WHERE `memberid` = %s"%(term,year,data['registerby'],data['proxytitle'],data['proxyname'],data['proxylastname'],data['memberid'])

            else:
                query2 = "UPDATE `shareholder%s/%s` SET `register` = '1', `registerby`= '%s', `registertime` = CURRENT_TIMESTAMP WHERE `memberid` = %s"%(term,year,data['registerby'],data['memberid'])
            cursor.execute(query2)
            conn.commit()
            query3 = 'SELECT * FROM `shareholder%s/%s` WHERE `memberid` = %s'%(term,year,data['memberid'])
            cursor.execute(query3)
            result = cursor.fetchone()
            columns = [column[0] for column in cursor.description]
            jsonResult = fetchOnetoJson(result,columns)
            returnData = {'status': 'success', 'info': jsonResult}

        except:
            returnData = {'status': 'fail', 'info': 'register error'}

    else:
        returnData = {'status': 'fail', 'info': 'Not found memberid :%s'%(data['memberid'])}

    cursor.close()
    return jsonify(returnData)
