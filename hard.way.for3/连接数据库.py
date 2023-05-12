# -*- coding: utf-8 -*-
import pymysql
config={
    "host":"192.168.6.24",
    "port":"3306",
    "user":"huaplus",
    "password":"Hangdong@3008",
    "database":"machine_learning"
}
db = pymysql.connect(**config)
cursor = db.cursor()
sql = "INSERT INTO `machine_learning`.`auth_group` (`id`, `name`) VALUES (%s, %s) "
cursor.execute(sql,(1,"bd"))
db.commit()  #提交数据
cursor.close()
db.close()