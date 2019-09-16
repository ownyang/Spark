#!/bin/bash

yum install -y python-pip
pip install flask
pip install pyOpenSSL
pip install flask-sqlalchemy

#wget http://repo.mysql.com/mysql-community-release-el7-5.noarch.rpm
rpm -ivh mysql-community-release-el7-5.noarch.rpm

yum install -y mysql
yum install -y mysql-server
yum install -y mysql-devel
yum install -y python-devel
yum install -y gcc
pip install MySQL-python 
