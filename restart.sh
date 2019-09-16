#!/bin/bash

pid=$(ps -ef |grep python |grep app.py | awk '{print $2}')
if(($? == 0))
then
    kill -9 $pid
fi

nohup python app.py > app.log 2>&1 &

