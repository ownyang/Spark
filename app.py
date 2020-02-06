#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, request
import json
import traceback
import sys
from flask_sqlalchemy import SQLAlchemy
import weixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from handler.user

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:Spark0111@localhost:9306/Spark?charset=utf8"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True 
db = SQLAlchemy(app)

TOKEN_SECRET = "Thisisspark-Secret-20200202"

@app.route('/api', methods=['POST'])
def apiDispatch():
    try:

        auth = request.authorization
        if not auth:
            return 'no authorization info', 401
        
        token = auth.username

        try:
            userInfo = verify_token(token)

        except Exception:
            return 'authorization fail', 401


        req = request.get_data()
        o = json.loads(req)
        action = o["action"]
        para = o.get('data', {})
        para['wxOpenId'] = userInfo['openid']
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

def create_token(openid):
    s = Serializer(TOKEN_SECRET, expires_in=86400*14)
    token = s.dumps({"openid":openid})

    return token

def verify_token(token):
    s = Serializer(TOKEN_SECRET)
    o = s.loads(token)

    return o



@app.route('/login', methods=['POST'])
def login():
    try:
        req = request.get_data()
        o = json.loads(req)
        code = o["code"]

        r = weixin.code2session(code)

        if r["errcode"] == 0:
            para = {"wxOpenId":r["openid"], "wxSessionKey":r["session_key"]}
            code, msg, data = handler.user.get(para)
            if data:
                #update
                handler.user.update(para)
            else:
                #add
                handler.user.add(para)
            
            token = create_token(r["openid"])

            resp = {
                "code" : 0,
                "msg" : 'ok',
                "data" : {"token":token}
            }

            return json.dumps(resp)

        else:
            return "request weixin fail. msg={0}".format(r["errmsg"]), 401

    except Exception:
        traceback.print_exc()
        return "exception", 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port = 443, ssl_context=('/data/release/spark/cert/1_api.sparkcharity.cn_bundle.crt', '/data/release/spark/cert/2_api.sparkcharity.cn.key'),  threaded=True)

