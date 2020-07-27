#!/usr/bin/python
# -*- coding: utf-8 -*-

from app import db 
from datetime import datetime, date
from .BaseModel import BaseModel

class ClassStudent(BaseModel):
    __tablename__ = "rClassStudent"
    classId = db.Column(db.Integer, primary_key = True)
    studentId = db.Column(db.Integer, primary_key = True)
    isFeedback = db.Column(db.Integer)
    mark = db.Column(db.Integer)
    improvements = db.Column(db.String)
