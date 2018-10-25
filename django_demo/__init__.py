# 如果使用pymysql作为django工程的数据库连接驱动,必须执行以下函数
import pymysql

pymysql.install_as_MySQLdb()
