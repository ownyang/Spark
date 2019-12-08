# Spark
支教小程序API

# 框架
API是以python的flask框架搭建，数据库的访问使用Sqlalchemy的orm库

## flask
* flask是一个web框架，可以快速搭建web服务。有url路由，模版等功能
* flask教程 https://www.w3cschool.cn/flask/
* 微信读书《Flask Web开发实战：入门 进阶与原理解析》
* Spark的API主要用到了@app.route的url路由，快速实现一个简单的http server。

## Sqlalchemy
* Sqlalchemy是一个python的ORM库。使用ORM库主要是为了sql的安全性。
* sqlalchemy简单教程： https://zhuanlan.zhihu.com/p/27400862
* sqlalchemy的数据类型: https://blog.csdn.net/aimill/article/details/81531499
* 详细的查询文档  https://www.cnblogs.com/dashuperfect/articles/11369010.html
* Spark通过sqlalchemy来进行数据库操作，每个表都对应一个类

# API协议
## 协议总览
**url**
```
https://localhost/api
```
https协议, 请求路径为/api。以POST方式请求，请求和返回为json格式。

**请求参数**

```
{
  "action": "student.add",
  "data": {
    "wxOpenId": "123123",
    "name": "yangshuai",
    "phone": "666666"
  }
}
```

请求参数分为两部分:
* action：action分为两部分 `module.method`，第一部分为module，第二部分为module对应的处理函数。
* data: 传入的参数

**响应参数**

```
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
```

响应参数分为三部分：
* code: 返回码。整型，返回0为成功，非0表示错误。 另外http的返回码非200，请求也是错误
* msg: 返回的错误消息
* data: 返回的数据

## 接口列表

接口|说明
---|----
volunteer.add|数据库中增加volunteer。wxOpenId,name是必须传入。与tVolunteer表对应
volunteer.get|查询volunteer。根据传入的id (插入时生成的自增ID)查询volunteer信息。与tVolunteer表对应
volunteer.update|更改volunteer的信息。id是必传的，更改指定id的信息。除了id和wxOpenId不可更改外，在data中的传入的字段都可以更改。与tVolunteer表对应
student.add|数据库中增加student。wxOpenId,name是必须传入。与tStudent表对应
student.get|查询student。根据id来查询student的信息。与tStudent表对应
student.update|更改student的信息。根据id来更新。与tStudent表对应
class.create|创建一个课程。name, startTime, endTime是必须的参数。与tClass表对应
class.get|拉取课程信息。传入的参数比较多，见下面的具体接口描述
class.update|更改课程信息。可以更改老师，课程时间。与tClass表对应。更改老师，可以用这个接口更改
class.getWithStudent| 根据class id获取班级报名的同学。详见接口描述
class.delete|根据class id删除课程。
class.studentSelectClass | 同学选课。传入的参数为classId, studentIds。studentIds为同学Id的数组。
class.studentUnSelectClass | 同学取消选课。传入的参数为classId, studentId。
class.studentSignIn|同学上课签到。传入的参数为classId, studentId。
class.studentGetClass | 获得同学已报名的课程。studentId为必须，其他参数见接口详细列表

###class.create
创建课程
例子
```
curl  -k -i https://localhost/api -d'{"action":"class.create", "data":{"name":"class for englist", "startTime":"2019-12-01 09:00:00", "endTime":"2019-12-01 10:00:00", "volunteerId":2}}'

-----------
{"msg": "sucess", "code": 0, "data": []}

```

### class.get
根据条件拉取课程信息。
入参

字段|类型|必须|说明
---|---|---|---
id | int| 否| 课程id
begin|string|否| 时间过滤开始时间，格式2019-10-01 10:00:00
end|string|否| 时间过滤结束时间，格式2019-10-01 10:00:00
volunteerId|int|否|老师的Id
name|string|否|课程名称
offset|int|否|分页查找的offset
limit|int|否|分页查找的limit

出参
data是数组，数组中每个字段为

字段|类型|说明
---|---|---
id|int|课程id
name|string|课程名称
startTime|string|课程开始时间
endTime|string|课程结束时间
volunteerId|int|老师的Id
volunteerOpenId|string|老师的openId
volunteerName|string|老师的名称

例子
```
curl  -k -i https://localhost/api -d'{"action":"class.get", "data":{"limit":2, "offset":0, "begin":"2019-12-01 10:00:00"}}'

-------------
{"msg": "ok", "code": 0, "data": [{"volunteerOpenId": "123123", "name": "ownyang", "volunteerId": 2, "volunteerName": "yangshuai", "startTime": "2019-12-10 10:00:00", "endTime": "2019-12-10 12:00:00", "id": 1}]}
```

### class.getWithStudent
拉取具体某个课程的同学
入参

字段|类型|必须|说明
---|---|---|---
id|int|是|课程的id

出参数
返回的class信息，包含了class.get中的信息。另外增加了students字段，这是个数组，数组元素为学生信息。

字段|类型|说明
---|---|---
studentId|int|学生的Id
studengOpenId|stirng|学生的openId
studentName|string|学生的名称


例子
```
curl  -k -i https://localhost/api -d'{"action":"class.getWithStudent", "data":{"id":1}}'

-----------------
{"msg": "ok", "code": 0, "data": {"volunteerOpenId": "123123", "name": "ownyang", "students": [{"studentId": 1, "studentOpenId": "123123", "studentName": "yangshuai"}, {"studentId": 2, "studentOpenId": "", "studentName": ""}, {"studentId": 3, "studentOpenId": "", "studentName": ""}], "volunteerId": 2, "volunteerName": "yangshuai", "startTime": "2019-12-10 10:00:00", "endTime": "2019-12-10 12:00:00", "id": 1}}
```

### class.studentGetClass
拉取具体某个同学的所选的课程
入参

字段|类型|必须|说明
---|---|---|---
studentId|int|是|学生的id
begin|string|否| 时间过滤开始时间，格式2019-10-01 10:00:00
end|string|否| 时间过滤结束时间，格式2019-10-01 10:00:00
offset|int|否|分页查找的offset
limit|int|否|分页查找的limit

出参数
data是数组，数组元素为课程信息，字段为

字段|类型|说明
---|---|---
classId|int|课程id
className|string|课程名称
startTime|string|课程开始时间
endTime|string|课程结束时间
volunteerId|int|老师的Id
volunteerName|string|老师的名称
studentId|int|学生的Id
studentName|string|学生的名称
state|int|是否签到。0:未签到； 1:签到



例子
```
curl  -k -i https://localhost/api -d'{"action":"class.studentGetClass", "data":{"studentId":1}}'

-----------------
{"msg": "ok", "code": 0, "data": [{"classId": 1, "studentId": 1, "volunteerId": 2, "className": "ownyang", "state": 0, "studentName": "yangshuai", "volunteerName": "yangshuai", "startTime": "2019-12-10 10:00:00", "endTime": "2019-12-10 12:00:00"}]}

```





# 代码结构
* app.py  flask的http请求入口处理。将/api的请求，路由到apiDispatch函数处理。根据action找到handler/中的处理module
* handler/volunteer.py  处理action=volunteer.xxxx 的消息。
* handler/student.py  处理action=student.xxxx 的消息。
* handler/class.py  课程相关的接口
* model/Volunteer.py  Volunteer的model类，对应数据库中tVolunteer表。是Sqlalchemy的orm对应的类。 handler/volunteer.py会import这个文件，操作数据库.
* model/Student.py  Student的model类，对应数据库中Student表。是Sqlalchemy的orm对应的类。 handler/student.py会import这个文件，操作数据库.
* model/Class.py  Class的model类，对应数据库中Class表。是Sqlalchemy的orm对应的类。 handler/class.py会import这个文件，操作数据库.
* model/ClassStudent.py  ClassStudent的model类，对应数据库中ClassStuent表, 学生课程关系表。是Sqlalchemy的orm对应的类。 handler/class.py会import这个文件，操作数据库.
* restart.sh  简单重启webserver的脚本

# 数据库表设计
根据设计文档，创建了tVolunteer和tStudent两张表
```
CREATE TABLE IF NOT EXISTS `tVolunteer` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `wxOpenId` varchar(128) NOT NULL,
  `name` varchar(128) NOT NULL,
  `gende` enum('MAN','WOMEN') DEFAULT NULL,
  `birthday` date DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `school` varchar(128) DEFAULT NULL,
  `age` int(11) DEFAULT NULL,
  `qq` varchar(32) DEFAULT NULL,
  `parentName` varchar(128) DEFAULT NULL,
  `parentPhone` varchar(20) DEFAULT NULL,
  `parentJob` varchar(128) DEFAULT NULL,
  `studyAbroad` varchar(128) DEFAULT NULL,
  `teachExpirence` text,
  `advice` text,
  `hoby` varchar(128) DEFAULT NULL,
  `socialExpirence` text,
  `department` varchar(128) DEFAULT NULL,
  `applyDate` datetime DEFAULT NULL,
  `applySchedule` enum('DOING','DONE','REJECT') DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

CREATE TABLE IF NOT EXISTS `tStudent` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `wxOpenId` varchar(128) NOT NULL,
  `name` varchar(128) NOT NULL,
  `gende` enum('MAN','WOMEN') DEFAULT NULL,
  `birthday` date DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `school` varchar(128) DEFAULT NULL,
  `grade` varchar(128) DEFAULT NULL,
  `qq` varchar(32) DEFAULT NULL,
  `parentName` varchar(128) DEFAULT NULL,
  `parentPhone` varchar(20) DEFAULT NULL,
  `parentJob` varchar(128) DEFAULT NULL,
  `applyDate` datetime DEFAULT NULL,
  `applySchedule` enum('DOING','DONE','REJECT') DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

CREATE TABLE IF NOT EXISTS `tClass` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  `volunteerId` int(11)  default 0,
  `startTime` datetime NOT NULL,
  `endTime` datetime NOT NULL,
  `createTime` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

CREATE TABLE IF NOT EXISTS `rClassStudent` (
  `classId` int(11) NOT NULL,
  `studentId` int(11) NOT NULL,
  `state` int(11) default 0,
  PRIMARY KEY (`classId`,`studentId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


```

数据库简要说明下

表|说明
---|---
tVolunteer|老师的表。wxOpenId 是唯一的。主键是自增的id，本系统建议使用id来传参数。
tStudent|学生的表。wxOpenId 是唯一的。主键是自增的id，本系统建议使用id来传参数。
tClass|课程表。主键id是自增的，其中volunteerId是老师的id，一个课程对应一个老师。
rClassStudent|课程和学生的关系表。主要是classId和studentId.

