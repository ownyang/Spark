#!/bin/bash

curdir=$(dirname $(which $0))
cd $curdir

curl -m 1 https://api.sparkcharity.cn/api |grep "405 Method Not"
if(($? == 0))
then
    exit 0
fi

pid=$(ps -ef |grep python |grep app.py | awk '{print $2}')
if(($? == 0))
then
    kill -9 $pid
fi

nohup python app.py > app.log 2>&1 &

