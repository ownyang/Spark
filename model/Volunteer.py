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
    gende = db.Column(db.String(10))
    birthday = db.Column(db.Date)
    phone = db.Column(db.String(20))
    school = db.Column(db.String(128))
    age = db.Column(db.Integer)
    qq = db.Column(db.String(32))
    parentName = db.Column(db.String(128))
    parentPhone = db.Column(db.String(20))
    parentJob = db.Column(db.String(128))
    studyAbroad = db.Column(db.String(128))
    teachExpirence = db.Column(db.Text)
    advice = db.Column(db.Text)
    hoby = db.Column(db.String(128))
    socialExpirence = db.Column(db.Text)
    department = db.Column(db.String(128))
    applyDate = db.Column(db.DateTime)
    applySchedule= db.Column(db.String(128))
        
    