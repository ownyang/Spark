#!/usr/bin/python
# -*- coding: utf-8 -*-

from app import db 
from datetime import datetime, date

class BaseModel(db.Model):
    __abstract__ = True
    def __getitem__(self, key):
        return self.__dict__[key]

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def toDict(self):
        #return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}
        d = {}
        for k in self.__table__.columns:
            o = getattr(self, k.name, None)
            if o:
                if isinstance(o, datetime):
                    d[k.name] = o.strftime("%Y-%m-%d %H:%M:%S")
                elif isinstance(o, date):
                    d[k.name] = o.strftime("%Y-%m-%d")
                else:
                    d[k.name] = o
            else:
                d[k.name] = None
        return d

    def getFields(self):
        return [c.name for c in self.__table__.columns]