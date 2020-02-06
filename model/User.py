#!/usr/bin/python
# -*- coding: utf-8 -*-

from app import db 
from datetime import datetime, date
from .BaseModel import BaseModel

class User(BaseModel):
    __tablename__ = "tUser"
    wxOpenId = db.Column(db.String(128), primary_key = True)    
    wxSessionKey = db.Column(db.String(128))
    role = db.Column(db.String(32))
    
    
    createTime = db.Column(db.DateTime)
    
        
    

