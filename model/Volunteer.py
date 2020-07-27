#!/usr/bin/python
# -*- coding: utf-8 -*-

from app import db 
from datetime import datetime, date
from .BaseModel import BaseModel

class Volunteer(BaseModel):
    __tablename__ = "tVolunteer"
    id = db.Column(db.Integer, primary_key = True)
    wxOpenId = db.Column(db.String(128))
    name = db.Column(db.String(128))
    gender = db.Column(db.String(10))
    birthday = db.Column(db.Date)
    phone = db.Column(db.String(20))
    school = db.Column(db.String(128))
    #age = db.Column(db.Integer)
    qq = db.Column(db.String(32))
    parentType = db.Column(db.String(10))
    parentName = db.Column(db.String(128))
    parentPhone = db.Column(db.String(20))
    department = db.Column(db.String(128))
    applyDate = db.Column(db.DateTime)
    applySchedule= db.Column(db.String(128))

    @staticmethod
    def getInfoById(ids):
        r = {}
        if not isinstance(ids, list):
            ids = [ids]
        
        try:
            res = db.session.query(Volunteer).filter(Volunteer.id.in_(ids)).all()
            if res:
                for i in res:
                    r[i['id']] = i.toDict()
                
            db.session.commit()
            
        except Exception as e:
            db.session.rollback()
            return -1 ,None
        return 0, r


        
    
