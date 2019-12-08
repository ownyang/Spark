#!/usr/bin/python
# -*- coding: utf-8 -*-

from app import db
import model.Student
import model.Volunteer
import model.Class
import model.ClassStudent
import datetime
import MySQLdb as mydb
import copy

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
    if "volunteerId" in para:
        volunteerId = int(para['volunteerId'])
        cond = cond + " and volunteerId={0}".format(volunteerId)
    if "name" in para:
        name = mydb.escape_string(para["name"])
        cond = cond + " and name = '{0}' ".format(name)
    if "begin" in para:
        begin = mydb.escape_string(para['begin'])
        cond = cond + " and startTime >= '{0}'".format(begin)
    if "end" in para:
        end = mydb.escape_string(para['end'])
        cond = cond + " and startTime <= '{0}'".format(end)
    sql = "select id, name, volunteerId, startTime, endTime from tClass where " + cond + " order by startTime desc "
    
    if "limit" in para:
        offset = int(para['offset']) if 'offset' in para else 0
        limit = int(para['limit'])
        sql = sql + " limit {0}, {1}".format(offset, limit)
    
    try:
        volIds = []
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
            r["volunteerOpenId"] = ""
            r["volunteerName"] = ""
            l.append(r)
            if i['volunteerId'] and i['volunteerId'] > 0:
                volIds.append(i['volunteerId'])
        
        #get volunteer info
        code, volInfos = model.Volunteer.Volunteer.getInfoById(volIds)
        if code == 0 and len(volInfos.keys()) > 0:
            for i in l:
                if i["volunteerId"] in volInfos:
                    volId = i["volunteerId"]
                    i['volunteerOpenId'] = volInfos[volId]["wxOpenId"]
                    i['volunteerName'] = volInfos[volId]["name"]
        
    except Exception as e:
        db.session.rollback()
        raise e
    db.session.commit()
    
    return 0, 'ok', l

def getWithStudent(para):
    r = {}
    id = int(para["id"])

    tPara = {"id":id}
    code, _, l = get(tPara)

    if len(l) > 0:
        r = l[0]
    
    #get studentIds from rClassStudent
    res = db.session.query(model.ClassStudent.ClassStudent).filter_by(classId=id).all()
    sIds = []
    students = []
    for i in res:
        sIds.append(i["studentId"])
        s = {}
        s["studentId"] = i["studentId"]
        s["studentOpenId"] = ""
        s["studentName"] = ""
        students.append(s)
    
    if len(sIds) > 0:
        code, sInfos = model.Student.Student.getInfoById(sIds)
    
    if code == 0 and len(sInfos.keys()) > 0:
        for i in students:
            sId = i["studentId"]
            if sId in sInfos:
                i["studentOpenId"] = sInfos[sId]["wxOpenId"]
                i["studentName"] = sInfos[sId]["name"]
    r["students"] = students

    return 0, 'ok', r


def update(para):
    id = para["id"]
    
    req = db.session.query(model.Class.Class).filter_by(id = id)

    

    update = {}
    v = req.first()
    if v is None:
        return 404, 'id not exist', []
    fields = v.getFields()
    for field in fields:
        if field in para and field not in ("id"):
            update[field] = para[field]
    try:
        req.update(update)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)
        return 500, "db fail", []

    return 0, 'sucess', None

def studentSelectClass(para):
    classId = para["classId"]
    studentIds = para["studentIds"]

    try:
        for studentId in studentIds:
            r = model.ClassStudent.ClassStudent(classId=classId, studentId = studentId, state =0)
            db.session.add(r)
        
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
    
    return 0, 'ok', []

def delete(para):
    id = para["id"]

    try:
        db.session.query(model.ClassStudent.ClassStudent).filter_by(classId=id).delete()
        db.session.query(model.Class.Class).filter_by(id=id).delete()

        db.session.commit()

        return 0, 'ok', []
    except Exception as e:
        db.session.rollback()
        raise e

def studentUnSelectClass(para):
    classId = para["classId"]
    studentId = para["studentId"]

    try:
        
        db.session.query(model.ClassStudent.ClassStudent).filter_by(classId=classId, studentId=studentId).delete()

        db.session.commit()

        return 0, 'ok', []
        
    except Exception as e:
        db.session.rollback()
        raise e

def studentSignIn(para):
    classId = para["classId"]
    studentId = para["studentId"]

    try:
        update = {"state":1}
        db.session.query(model.ClassStudent.ClassStudent).filter_by(classId=classId, studentId=studentId).update(update)

        db.session.commit()

        return 0, 'ok', []
        
    except Exception as e:
        db.session.rollback()
        raise e

def studentGetClass(para):
    studentId = int(para["studentId"])
    cond = " t2.studentId = {0} ".format(studentId)
    if "begin" in para:
        begin = mydb.escape_string(para['begin'])
        cond = cond + " and t1.startTime >= '{0}'".format(begin)
    if "end" in para:
        end = mydb.escape_string(para['end'])
        cond = cond + " and t1.startTime <= '{0}'".format(end)
    sql = "select t1.id classId, t1.name className, t1.volunteerId volunteerId, t1.startTime, t1.endTime, t4.name volunteerName, t2.studentId, t3.name studentName, t2.state from tClass t1, rClassStudent t2, tStudent t3, tVolunteer t4 where t1.id = t2.classId and t2.studentId = t3.id and t1.volunteerId = t4.id and   " + cond + " order by startTime desc "
    
    if "limit" in para:
        offset = int(para['offset']) if 'offset' in para else 0
        limit = int(para['limit'])
        sql = sql + " limit {0}, {1}".format(offset, limit)
    
    try:        
        cur = db.session.execute(sql)
        res = cur.fetchall()
        l = []
        for i in res:
            r = {}
            r['classId'] = i['classId']
            r['className'] = i['className']
            r["startTime"] = i["startTime"].strftime("%Y-%m-%d %H:%M:%S")
            r["endTime"] = i['endTime'].strftime("%Y-%m-%d %H:%M:%S")
            r['volunteerId'] = i['volunteerId']
            r['volunteerName'] =  i['volunteerName']
            r['studentId'] =  i['studentId']
            r['studentName'] =  i['studentName']
            r['state'] = i['state']

            l.append(r)
            
        
    except Exception as e:
        db.session.rollback()
        raise e
    db.session.commit()
    
    return 0, 'ok', l



