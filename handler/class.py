#!/usr/bin/python
# -*- coding: utf-8 -*-

from app import db
import model.Student
import model.Volunteer
import model.Class
import datetime
import MySQLdb as mydb

def create(para):
    name = para["name"]
    startTime = datetime.datetime.strptime(para["startTime"], "%Y-%m-%d %H:%M:%S")
    endTime = datetime.datetime.strptime(para["endTime"], "%Y-%m-%d %H:%M:%S")

    r = model.Class.Class(name=name, startTime = startTime, endTime = endTime)

    if "volunteerId" in para:
        r["volunteerId"] = para["volunteerId"]
    
    try:
        db.session.add(r)
        db.session.commit()
        return 0, 'sucess', []
    except Exception as e:
        db.session.rollback()
        print(e)
        return 500, 'db fail', []

def get(para):
    cond = " 1 = 1"
    if "id" in para:
        id = int(para['id'])
        cond = cond + " and id={0}".format(id)
    if "begin" in para:
        begin = mydb.escape_string(para['begin'])
        cond = cond + " and startTime >= '{0}'".format(begin)
    if "end" in para:
        end = mydb.escape_string(para['end'])
        cond = cond + " and startTime <= '{0}'".format(end)
    sql = "select id, name, volunteerId, startTime, endTime from tClass where " + cond + " order by startTime "
    
    if "limit" in para:
        offset = int(para['offset']) if offset in para else 0
        limit = int(para['limit'])
        sql = sql + " limit {0}, {1}".format(offset, limit)
    
    try:
        cur = db.session.execute(sql)
        res = cur.fetchall()
        l = []
        for i in res:
            r = {}
            r["id"] = i["id"]
            r["name"] = i["name"]
            r["volunteerId"] = i["volunteerId"]
            r["startTime"] = i["startTime"].strftime("%Y-%m-%d %H:%M:%S")
            r["endTime"] = i['endTime'].strftime("%Y-%m-%d %H:%M:%S")
            l.append(r)
    except Exception as e:
        db.session.rollback()
        raise e
    db.session.commit()
    
    return 0, 'ok', l

    

    
