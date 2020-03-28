#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2
import json
import app
import time
weixinUrl = "https://api.weixin.qq.com"
appid = "wxf596e5ef09f5be7f"
secret = "8fecf2a920b6ae977e4e7d888fa8569d"

'''
docs
https://developers.weixin.qq.com/miniprogram/dev/api-backend/open-api/login/auth.code2Session.html
'''
def code2session(code):
    url = "{0}/sns/jscode2session?appid={1}&secret={2}&js_code={3}&grant_type=authorization_code".format(weixinUrl, appid, secret, code)
    try:
        app.mylogger.info("url={0}".format(url))
        req = urllib2.urlopen(url)
        resp = req.read()
        app.mylogger.info("resp={0}".format(resp))

        o = json.loads(resp)
        #openid = "{0}thiscode{1}".format(code, int(time.time()))  #mock
        #o = {"errcode":0, "errmsg":"ok", "openid":openid, "session_key":openid} #mock

        return o


    except Exception as e:
        raise e
    


