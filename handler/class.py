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
from app import mylogger

def create(para):
    classTime = datetime.datetime.strptime(para["classTime"], "%Y-%m-%d")

    r = model.Class.Class(classTime=classTime)

    if "volunteerId" in para:
        r["volunteerId"] = para["volunteerId"]
    
    if "createTime" in para:
        r["createTime"]=para["createTime"]

    r["isFeedback"]=0
    r["classBehavior"]=""
    r["classContent"]=""
    r["improvements"]=""
    r["changes"]=""
    r["notes"]=""
    
    try:
        db.session.add(r)
        db.session.commit()
        return 0, 'sucess', []
    except Exception as e:
        db.session.rollback()
        print(e)
        mylogger.info(e)
        return 500, 'db fail', []

def get(para):
    cond = " 1 = 1"
    if "id" in para:
        id = int(para['id'])
        cond = cond + " and id={0}".format(id)
    if "volunteerId" in para:
        volunteerId = int(para['volunteerId'])
        cond = cond + " and volunteerId={0}".format(volunteerId)
    if "begin" in para:
        begin = mydb.escape_string(para['begin'])
        cond = cond + " and classTime >= '{0}'".format(begin)
    if "end" in para:
        end = mydb.escape_string(para['end'])
        cond = cond + " and classTime <= '{0}'".format(end)
    sql = "select id,  volunteerId, classTime, isFeedback, classBehavior, classContent, improvements, changes, notes from tClass where " + cond + " order by classTime desc "
    mylogger.info(sql)
    
    if "limit" in para:
        offset = int(para['offset']) if 'offset' in para else 0
        limit = int(para['limit'])
        sql = sql + " limit {0}, {1}".format(offset, limit)
    
    try:
        volIds = []
        cur = db.session.execute(sql)
        res = cur.fetchall()
        l = []
        mylogger.info(res)
        for i in res:
            r = {}
            id = r["id"] = i["id"]
            #r["name"] = i["name"]
            r["volunteerId"] = i["volunteerId"]
            r["classTime"] = i["classTime"].strftime("%Y-%m-%d")
            r["isFeedback"] = i['isFeedback']
            r["classBehavior"] = i["classBehavior"]
            r["classContent"] = i["classContent"]
            r["improvements"] = i["improvements"]
            r["changes"] = i["changes"]
            r["notes"] = i["notes"]
            r["volunteerName"] = ""
            r["volunteerOpenId"] = ""
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
        '''
        #get student info
        for i in l:
            res=db.session.query(model.ClassStudent.ClassStudent).filter_by(classId=id).all()
            sids=[]
            for j in res:
                sids.append(j['studentId'])
            if len(sids)>0:
                code, sinfos=model.Student.Student.getInfoById(sids)
            if code==0 and len(sids) > 0 and sInfos and  len(sInfos.keys())>0:
                for j in sids:
                    sid=j
                    if sid in sinfos:
                        i['studentName']=sinfos[sid]['name']
        '''
    except Exception as e:
        db.session.rollback()
        raise e
    db.session.commit()
    
    return 0, 'ok', l

def getStudent(para):
    r = {}
    id = int(para["id"])

    #get studentIds from rClassStudent
    res = db.session.query(model.ClassStudent.ClassStudent).filter_by(classId=id).all()
    sIds = []
    students = []
    for i in res:
        sIds.append(i["studentId"])
        s = {}
        s["studentId"] = i["studentId"]
        s["isFeedback"] = i["isFeedback"]
        s["mark"] = i["mark"]
        s["improvements"] = i["improvements"]
        s["studentOpenId"] = ""
        s["studentName"] = ""
        students.append(s)
    
    code=-1
    sInfos=None
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
    studentId = para["studentId"]

    try:
        r = model.ClassStudent.ClassStudent(classId=classId, studentId = studentId)
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

def studentGetClass(para):
    studentId = int(para["studentId"])
    cond = " t2.studentId = {0} ".format(studentId)
    if "begin" in para:
        begin = mydb.escape_string(para['begin'])
        cond = cond + " and t1.classTime >= '{0}'".format(begin)
    if "end" in para:
        end = mydb.escape_string(para['end'])
        cond = cond + " and t1.classTime <= '{0}'".format(end)
    if "classId" in para:
        cond = cond + " and t1.classId = '{0}'".format(para["classId"])
    sql = "select t1.id classId, t1.volunteerId volunteerId, t1.classTime, t4.name volunteerName, t2.studentId, t3.name studentName, t2.isFeedback, t2.mark, t2.improvements from tClass t1, rClassStudent t2, tStudent t3, tVolunteer t4 where t1.id = t2.classId and t2.studentId = t3.id and t1.volunteerId = t4.id and   " + cond + " order by classTime desc "
    
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
            r["classTime"] = i["classTime"].strftime("%Y-%m-%d %H:%M:%S")
            r['volunteerId'] = i['volunteerId']
            r['volunteerName'] =  i['volunteerName']
            r['studentId'] =  i['studentId']
            r['studentName'] =  i['studentName']
            r['isFeedback'] = i['isFeedback']
            r['mark'] = i['mark']
            r['improvements'] = i['improvements']

            l.append(r)
            
        
    except Exception as e:
        db.session.rollback()
        raise e
    db.session.commit()
    
    return 0, 'ok', l
 
def feedback(para):
    studentId = para["studentId"]
    classId = para["classId"]
    
    req = db.session.query(model.ClassStudent.ClassStudent).filter_by(classId = classId).filter_by(studentId = studentId)

    update = {}
    v = req.first()
    if v is None:
        return 404, 'id not exist', []
    fields = v.getFields()
    for field in fields:
        if field in para and field not in ("studentId", "classId"):
            update[field] = para[field]
    try:
        req.update(update)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        mylogger.info(e)
        return 500, "db fail", []

    return 0, 'sucess', None



