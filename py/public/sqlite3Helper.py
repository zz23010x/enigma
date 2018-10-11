import os
import shutil
import sqlite3
from public.LogHelper import logger

class DataBaseServer(object):
    __instance = None

    def __init__(self):
        pass

    def __new__(cls, *args, **kwd):
        if DataBaseServer.__instance is None:
            DataBaseServer.__instance = object.__new__(cls, *args, **kwd)
            DataBaseServer.__instance.__dbserver = SqliteHelper()
            if not os.path.isdir(os.path.join(os.getcwd(), 'db')):
                os.mkdir('db')
            cls.__filepath = os.path.join(os.getcwd(), 'db', 'value.db')
            DataBaseServer.__instance.__dbserver.SetPath(cls.__filepath)
            if not os.path.exists(cls.__filepath):
                shutil.copy(os.path.join(os.getcwd(), 'db.sqlite3'), cls.__filepath)
                cls.DropAllTables()
            cls.__startDBServerModule(cls)
            DataBaseServer.__instance.__dbserver.listTablename()
        return DataBaseServer.__instance

    def __startDBServerModule(self):
        self.__CreateTable(self)

    def __CreateTable(self):
        if not DataBaseServer.__instance.__dbserver.isExistsTable('tab_job_info_zhilian'):
            job_info_zhilian = '''create table tab_job_info_zhilian(id int not null, number text primary key, info text, keyword text)'''
            DataBaseServer.__instance.__dbserver.sqlExec(job_info_zhilian)
        if not DataBaseServer.__instance.__dbserver.isExistsTable('tab_shop_item_info'):
            shop_item_info = '''create table tab_shop_item_info(id int not null primary key, name text not null, price number not null)'''
            DataBaseServer.__instance.__dbserver.sqlExec(shop_item_info)

    def InsertValues(self, sqlstr, args=None):
        DataBaseServer.__instance.__dbserver.sqlExec(sqlstr, args)
        logger().info('[DB Write Value]-[0]'.format(sqlstr))

    def SelectTable(self, sqlstr):
        return DataBaseServer.__instance.__dbserver.sqlExec(sqlstr)

    def DropAllTables(self):
        DataBaseServer.__instance.__dbserver.clearTable()        

class SqliteHelper:
    def  __init__(self):
        self.path = None

    def SetPath(self, path):
        self.path = path
    
    def CheckPathDB(self):
        if self.path is None:
            return False

        if not os.path.exists(self.path):
            return False

        return True

    def SqlConsole(self):
        try:
            while(True):
                command = input('input:')
                if command == 'exit':
                    break
                self.ConnectDb()
                cur = self.conn.cursor()
                cur.execute(command)
                print(cur.fetchall())
        except Exception as e:
            print('error:' + str(e))
        finally:
            self.conn.commit()
            self.ConnectClose()
    
    def sqlExec(self, sqlstr, args=None):
        if self.CheckPathDB():
            conn = sqlite3.connect(self.path)
            cur = conn.cursor()
            if args == None:
                cur.execute(sqlstr)
            else:
                cur.executemany(sqlstr, args)
            conn.commit()
            result = cur.fetchall()
            conn.close()
            return result
        
    def sqlExecSeq(self, sqllist):
        self.ConnectDb()
        cur = self.conn.cursor()
        for sql in sqllist:
            cur.execute(sql)
        self.conn.commit()
        self.ConnectClose()

    def listTablename(self):
        if self.CheckPathDB():
            conn = sqlite3.connect(self.path)
            result = conn.cursor().execute('SELECT name FROM sqlite_master WHERE type="table" ORDER BY name').fetchall()
            conn.close()
            return result
    
    def isExistsTable(self, tablename):
        for tab in self.listTablename():
            if tab[0] == tablename:
                return True
        return False

    def clearTable(self):
        for item in self.listTablename():
            if item[0] == 'sqlite_sequence':
                continue
            self.sqlExec('drop table %s' %(item[0]))

a = DataBaseServer()