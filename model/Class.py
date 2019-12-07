#!/usr/bin/python
# -*- coding: utf-8 -*-

from app import db 
from datetime import datetime, date
from .BaseModel import BaseModel

class Class(BaseModel):
    __tablename__ = "tClass"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(128))
    volunteerId = db.Column(db.Integer)
    
    startTime = db.Column(db.DateTime)
    endTime = db.Column(db.DateTime)
    createTime = db.Column(db.DateTime)
    
        
    

