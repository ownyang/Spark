#!/usr/bin/python
# -*- coding: utf-8 -*-

from app import db
import model.Student

def add(para):
    wxOpenId = str(para["wxOpenId"])
    name = para["name"]
    r = model.Student.Student(wxOpenId=wxOpenId, name=name)
    fields = r.getFields()
    for f in fields:
        if f in para:
            r[f] = para[f]
    try:
        db.session.add(r)
        db.session.commit()
        return 0, 'sucess', []
    except Exception as e:
        db.session.rollback()
        print(e)
        return 500, 'db fail', []

def get(para):
    id = para["id"]
    v = db.session.query(model.Student.Student).filter_by(id = id).first()

    return 0,'sucess',  v.toDict()

def update(para):
    id = para["id"]
    
    req = db.session.query(model.Student.Student).filter_by(id = id)

    update = {}
    v = req.first()
    if v is None:
        return 404, 'id not exits', []
    fields = v.getFields()
    for field in fields:
        if field in para and field not in ("id", "wxOpenId"):
            update[field] = para[field]
    try:
        req.update(update)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)
        return 500, "db fail", []

    return 0, 'sucess', None

    
