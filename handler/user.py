#!/usr/bin/python
# -*- coding: utf-8 -*-

from app import db
import model.User

def add(para):
    wxOpenId = str(para["wxOpenId"])
    wxSessionKey = para["wxSessionKey"]
    r = model.User.User(wxOpenId=wxOpenId, wxSessionKey=wxSessionKey)
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
    wxOpenId = para["wxOpenId"]
    v = db.session.query(model.User.User).filter_by(wxOpenId = wxOpenId).first()
    if v:
        return 0,'sucess',  v.toDict()
    else:
        return 0, 'success', {}

def update(para):
    wxOpenId = para["wxOpenId"]
    
    req = db.session.query(model.User.User).filter_by(wxOpenId = wxOpenId)

    update = {}
    v = req.first()
    if v is None:
        return 404, 'id not exits', []
    fields = v.getFields()
    for field in fields:
        if field in para and field not in ("wxOpenId"):
            update[field] = para[field]
    try:
        req.update(update)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)
        return 500, "db fail", []

    return 0, 'sucess', None

    
