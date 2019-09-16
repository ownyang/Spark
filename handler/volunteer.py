#!/usr/bin/python
# -*- coding: utf-8 -*-

from app import db
import model.Volunteer

def add(para):
    wxOpenId = str(para["wxOpenId"])
    name = para["name"]
    r = model.Volunteer.Volunteer(wxOpenId=wxOpenId, name=name)
    fields = r.getFields()
    for f in fields:
        if f in para:
            r[f] = para[f]
    db.session.add(r)
    db.session.commit()
    return 0, 'sucess', []

def get(para):
    id = para["id"]
    v = db.session.query(model.Volunteer.Volunteer).filter_by(id = id).first()

    return 0,'sucess',  v.toDict()

def update(para):
    id = para["id"]
    
    req = db.session.query(model.Volunteer.Volunteer).filter_by(id = id)

    update = {}
    v = req.first()
    fields = v.getFields()
    for field in fields:
        if field in para and field not in ("id", "wxOpenId"):
            update[field] = para[field]
    req.update(update)

    db.session.commit()

    return 0, 'sucess', None
