#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2
import json

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
        print("url={0}".format(url))
        req = urllib2.urlopen(url)
        resp = req.read()
        print("resp={0}".format(resp))

        o = json.loads(resp)

        return o


    except Exception as e:
        raise e
    


