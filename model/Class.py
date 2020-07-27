#!/usr/bin/python
# -*- coding: utf-8 -*-

from app import db 
from datetime import datetime, date
from .BaseModel import BaseModel

class Class(BaseModel):
    __tablename__ = "tClass"
    id = db.Column(db.Integer, primary_key = True)
    volunteerId = db.Column(db.Integer)
    classTime = db.Column(db.Date)
    createTime = db.Column(db.DateTime)
    isFeedback = db.Column(db.Integer)
    classBehavior = db.Column(db.String)
    classContent = db.Column(db.String)
    improvements = db.Column(db.String)        
    changes = db.Column(db.String)
    notes = db.Column(db.String)
