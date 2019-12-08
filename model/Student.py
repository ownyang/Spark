#!/usr/bin/python
# -*- coding: utf-8 -*-

from app import db 
from datetime import datetime, date
from .BaseModel import BaseModel

class Student(BaseModel):
    __tablename__ = "tStudent"
    id = db.Column(db.Integer, primary_key = True)
    wxOpenId = db.Column(db.String(128))
    name = db.Column(db.String(128))
    gende = db.Column(db.String(10))
    birthday = db.Column(db.Date)
    phone = db.Column(db.String(20))
    school = db.Column(db.String(128))
    grade = db.Column(db.String(128))
    qq = db.Column(db.String(32))
    parentName = db.Column(db.String(128))
    parentPhone = db.Column(db.String(20))
    parentJob = db.Column(db.String(128))
    applyDate = db.Column(db.DateTime)
    applySchedule= db.Column(db.String(128))

    @staticmethod
    def getInfoById(ids):
        r = {}
        if not isinstance(ids, list):
            ids = [ids]
        
        try:
            res = db.session.query(Student).filter(Student.id.in_(ids)).all()
            if res:
                for i in res:
                    r[i['id']] = i.toDict()
                
            db.session.commit()
            
        except Exception as e:
            db.session.rollback()
            return -1 ,None
        return 0, r
        
    

