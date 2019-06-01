# -*- coding: utf-8 -*-
#
import pymysql
class DataBaseHandle(object):
    ''' 定义一个 MySQL 操作类'''
    def __init__(self, host='localhost', username='root', password='nopwd@mysql', database='tushare', port=3306):
        '''初始化数据库信息并创建数据库连接'''
        # 下面的赋值其实可以省略，connect 时 直接使用形参即可
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.port = port
        try:
            self.db = pymysql.connect(self.host,self.username,self.password,self.database,self.port,charset='utf8')
        except:
            raise "DataBase connect error,please check the db config."
        



    #  这里 注释连接的方法，是为了 实例化对象时，就创建连接。不许要单独处理连接了。
    #
    # def connDataBase(self):
    #     ''' 数据库连接 '''
    #
    #     self.db = pymysql.connect(self.host,self.username,self.password,self.port,self.database)
    #
    #     # self.cursor = self.db.cursor()
    #
    #     return self.db

    def createLibrary(self, name):
        '''创建库'''
        
        sql_cmd = "CREATE DATABASE IF NOT EXISTS {}".format(name)
        print('创建库',sql_cmd)

        self.cursor = self.db.cursor()
        try:
            self.cursor.execute(sql_cmd)
        except Exception as e:
            print('error:', e)
            # 发生错误时回滚
            self.db.rollback()
        finally:
            self.cursor.close()

    def createTable(self, tablename, *params):
        '''创建表'''
        title_lst = ''
        for i in range(len(params)):
            if i == len(params) - 1:
                title_lst += "{0} VARCHAR(20) NOT NULL".format(params[i])
            else:
                title_lst += "{0} VARCHAR(20) NOT NULL,".format(params[i])
        sql_cmd = "CREATE TABLE IF NOT EXISTS {0} ({1}) DEFAULT CHARSET=UTF8MB4;".format(tablename, title_lst)
        print('创建表',sql_cmd)
        self.cursor = self.db.cursor()
        try:
            # 执行sql
            self.cursor.execute(sql_cmd)
            # tt = self.cursor.execute(sql)  # 返回 插入数据 条数 可以根据 返回值 判定处理结果
            # print(tt)
            self.db.commit()
        except Exception as e:
            print('error:', e)
            # 发生错误时回滚
            self.db.rollback()
        finally:
            self.cursor.close()

    def insertDB(self,tablename, **params):
        ''' 插入数据库操作 params--字典'''
        key_lst = ''
        value_lst = ''
        for key, value in params.items():
            if key == list(params.keys())[-1]:
                key_lst += key
                value_lst += "'{0}'".format(value) 
            else:
                key_lst += key + ','
                value_lst += "'{0}'".format(value)  + ','

        sql_cmd = "INSERT INTO {0} ({1}) VALUES ({2});".format(tablename, key_lst, value_lst)
        print('插入:', sql_cmd)
        self.cursor = self.db.cursor()
        try:
            # 执行sql
            self.cursor.execute(sql_cmd)
            # tt = self.cursor.execute(sql)  # 返回 插入数据 条数 可以根据 返回值 判定处理结果
            # print(tt)
            self.db.commit()
        except Exception as e:
            print('error:', e)
            # 发生错误时回滚
            self.db.rollback()
        finally:
            self.cursor.close()

    def deleteDB(self,tablename, istable=False,**params):
        ''' 操作数据库数据删除 '''
        print(params)
        if istable:
            sql_cmd = "DELETE FROM {0}".format(tablename)
        else:
            for k, v in params.items():
                sql_cmd = "DELETE FROM {0} WHERE {1}={2};".format(tablename, k, v)
        self.cursor = self.db.cursor()
        try:
            # 执行sql
            self.cursor.execute(sql_cmd)
            # tt = self.cursor.execute(sql) # 返回 删除数据 条数 可以根据 返回值 判定处理结果
            # print(tt)
            self.db.commit()
        except Exception as e:
            print('error:', e)
            # 发生错误时回滚
            self.db.rollback()
        finally:
            self.cursor.close()

    def updateDb(self,tablename,):
        ''' 更新数据库操作 '''

        self.cursor = self.db.cursor()

        try:
            # 执行sql
            self.cursor.execute(sql)
            # tt = self.cursor.execute(sql) # 返回 更新数据 条数 可以根据 返回值 判定处理结果
            # print(tt)
            self.db.commit()
        except Exception as e:
            print('error:', e)
            # 发生错误时回滚
            self.db.rollback()
        finally:
            self.cursor.close()

    def selectDb(self,sql):
        ''' 数据库查询 '''
        self.cursor = self.db.cursor()
        try:
            self.cursor.execute(sql) # 返回 查询数据 条数 可以根据 返回值 判定处理结果

            data = self.cursor.fetchall() # 返回所有记录列表

            print(data)

            # 结果遍历
            for row in data:
                sid = row[0]
                name = row[1]
                # 遍历打印结果
                print('sid = %s,  name = %s'%(sid,name))
        except Exception as e:
            print('error:', e)
            print('Error: unable to fecth data')
        finally:
            self.cursor.close()


    def closeDb(self):
        ''' 数据库连接关闭 '''
        self.db.close()