#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, request
import json
import traceback
import sys
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:Spark0111@localhost:9306/Spark?charset=utf8"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True 
db = SQLAlchemy(app)

@app.route('/api', methods=['POST'])
def apiDispatch():
    try:
        req = request.get_data()
        o = json.loads(req)
        action = o["action"]
        para = o['data']
        l = action.split(".")
        mName, fName = l[0], l[1]
        mName = "handler." + mName
        __import__(mName)
        if mName not in sys.modules:
            return "action not found", 405

        m = sys.modules[mName]
        reload(m)
        f = getattr(m, fName, None)
        if not callable(f):
            return "handler not found", 405
        
        code, msg, data = f(para)

        resp = {
            "code" : code,
            "msg" : msg,
            "data" : data if data else []
        }

        return json.dumps(resp)


    except Exception:
        traceback.print_exc()
        return "exception", 500


if __name__ == "__main__":
    app.run(port = 443, ssl_context='adhoc')

