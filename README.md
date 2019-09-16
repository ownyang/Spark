# Spark
支教小程序API

# 框架
API是以python的flask框架搭建，数据库的访问使用Sqlalchemy的orm库

## flask
flask是一个web框架，可以快速搭建web服务。有url路由，模版等功能
flask教程 https://www.w3cschool.cn/flask/
微信读书《Flask Web开发实战：入门 进阶与原理解析》
Spark的API主要用到了@app.route的url路由，快速实现一个简单的http server。

## Sqlalchemy
Sqlalchemy是一个python的ORM库。使用ORM库主要是为了sql的安全性。
sqlalchemy简单教程： https://zhuanlan.zhihu.com/p/27400862
sqlalchemy的数据类型: https://blog.csdn.net/aimill/article/details/81531499
Spark通过sqlalchemy来进行数据库操作，每个表都对应一个类

# API协议
## 协议总览
**url**
'''
https://localhost/api
'''
https协议, 请求路径为/api。以POST方式请求，请求和返回为json格式。

**请求参数**

···
{
  "action": "student.add",
  "data": {
    "wxOpenId": "123123",
    "name": "yangshuai",
    "phone": "666666"
  }
}
···

请求参数分为两部分:
* action：action分为两部分 `module.method`，第一部分为module，第二部分为module对应的处理函数。
* data: 传入的参数

**响应参数**

···
{
  "msg": "sucess",
  "code": 0,
  "data": {
    "qq": null,
    "school": null,
    "studyAbroad": null,
    "name": "yangshuai",
    "hoby": null,
    "age": null,
    "parentName": null,
    "department": null,
    "id": 3,
    "phone": "666666",
    "birthday": "2019-08-01",
    "socialExpirence": null,
    "advice": "xxxxxx",
    "teachExpirence": null,
    "parentJob": null,
    "applyDate": "2019-09-15 00:00:00",
    "wxOpenId": "123123",
    "gende": "MAN",
    "applySchedule": null,
    "parentPhone": null
  }
}
···

响应参数分为三部分：
* code: 返回码。整型，返回0为成功，非0表示错误。 另外http的返回码非200，请求也是错误
* msg: 返回的错误消息
* data: 返回的数据

##接口列表
>已经示例写了volunteer和student的接口，包括增，改，查

接口|说明
---|----
volunteer.add|数据库中增加volunteer。wxOpenId,name是必须传入
volunteer.get|查询volunteer。根据传入的id (插入时生成的自增ID)查询volunteer信息
volunteer.update|更改volunteer的信息。id是必传的，更改指定id的信息。除了id和wxOpenId不可更改外，在data中的传入的字段都可以更改

