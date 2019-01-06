# -*- coding: utf-8 -*-

import sqlite3
import codecs
import os

# 生成python字典
def generateDict(tableName):
    # 列标题
    cur.execute("select * from %s" % tableName)
    colKeys = [key[0] for key in cur.description]

    # 列属性，未使用，可以通过sqlite中表的列属性用来判断是int还是text
    # attrs = cur.execute("PRAGMA table_info(city_ui)").fetchall()

    # 数据
    # data = cur.execute("select * from %s" % tableName).fetchall()
    dataTmp = cur.execute("select * from %s" % tableName).fetchall()
    data = []
    for row in dataTmp:
        dataChild = []
        for child in row:
            dataChild.append(child)
        data.append(dataChild)

    colAttriDict = {}
    # 先判断是不是二维数组
    for index in range(len(colKeys)):
        for line in data:
            if type(line[index]) == str:
                if line[index].find('^') != -1:
                    colAttriDict[index] = 'vec2'
                    break
    # 在判断是不是数组
    for index in range(len(colKeys)):
        for line in data:
            if type(line[index]) == str:
                if (line[index].find('|') != -1 or line[index].find('&') != -1) and (index in colAttriDict) == False:
                    colAttriDict[index] = 'vec1'
                    break
    # 剩下的都是normal
    for index in range(len(colKeys)):
        if (index in colAttriDict) == False:
            colAttriDict[index] = 'normal'

    # for line in colAttriDict:
    #     print ('%s  %s' % (line, colAttriDict[line]))

    dictTmp = {}
    for i in data:
        i[0] = int(i[0])
        dictTmp[i[0]] = {}
        for j in range(len(i)):
            # Todo，默认使用第一列作为下标
            if colAttriDict[j] == 'normal':
                valueTmp = i[j]
                dictTmp[i[0]][colKeys[j]] = getFilePath(valueTmp, filePathDict)
            elif colAttriDict[j] == 'vec1':
                if i[j].find('&') != -1:
                    dictTmp[i[0]][colKeys[j]] = i[j].split("&")
                    for idx in range(len(dictTmp[i[0]][colKeys[j]])):
                        valueTmp = dictTmp[i[0]][colKeys[j]][idx]
                        dictTmp[i[0]][colKeys[j]][idx] = getFilePath(valueTmp, filePathDict)
                else:
                    dictTmp[i[0]][colKeys[j]] = i[j].split("|")
                    for idx in range(len(dictTmp[i[0]][colKeys[j]])):
                        valueTmp = dictTmp[i[0]][colKeys[j]][idx]
                        dictTmp[i[0]][colKeys[j]][idx] = getFilePath(valueTmp, filePathDict)
            elif colAttriDict[j] == 'vec2':
                dictTmp[i[0]][colKeys[j]] = i[j].split("^")
                vec2Tmp = dictTmp[i[0]][colKeys[j]]
                for k in range(len(vec2Tmp)):
                    if dictTmp[i[0]][colKeys[j]][k].find('&') != -1:
                        dictTmp[i[0]][colKeys[j]][k] = dictTmp[i[0]][colKeys[j]][k].split('&')
                        for idx in range(len(dictTmp[i[0]][colKeys[j]][k])):
                            valueTmp = dictTmp[i[0]][colKeys[j]][k][idx]
                            dictTmp[i[0]][colKeys[j]][k][idx] = getFilePath(valueTmp, filePathDict)
                    else:
                        dictTmp[i[0]][colKeys[j]][k] = dictTmp[i[0]][colKeys[j]][k].split('|')
                        for idx in range(len(dictTmp[i[0]][colKeys[j]][k])):
                            valueTmp = dictTmp[i[0]][colKeys[j]][k][idx]
                            dictTmp[i[0]][colKeys[j]][k][idx] = getFilePath(valueTmp, filePathDict)
            else:
                pass

    # for line in dictTmp:
    #     print(dictTmp[line])

    return dictTmp

def getFilePath(valueCur, valueDict):
    try:
        valueCur.find('.png')
    except AttributeError:
        print ('')
    else:
        if valueCur.find('.png') != -1 or valueCur.find('.sprite') != -1:
            keyListTmp = valueCur.split('/')
            keyTmp = keyListTmp[-1]
            if (keyTmp in valueDict) == True:
                try:
                    valueCur = valueDict[keyTmp]
                except TypeError:
                    pass
    return valueCur

def getFilePathDict():
    pathDict = {}
    for dirpath, dirnames, filenames in os.walk('..\\ccbResources'):
        for fname in filenames:
            if dirpath.find('.svn') == -1:
                pathList = dirpath.split("\\")
                localPath = pathList[-2] + '/' + pathList[-1] + '/' + fname
                pathDict[fname] = localPath

    return pathDict

def writeWithList(keyValue):
    pass

def writeWithStr(keyValue):
    pass

# 将字典写入lua
def writeDict2Lua(dictTmp, tableName):
    out = codecs.open('%s.lua' % tableName, 'w', encoding='utf-8')

    out.write('CSV.tables.%s = {\n' % tableName)
    for key1 in sorted(dictTmp.keys()):
        out.write('\t[%s] = {\n' % str(key1))
        for key2 in sorted(dictTmp[key1]):
            if type(dictTmp[key1][key2]) != list:
                # 判断是否是'123'类型的字符串
                # 非'123'字符串需要加上("")写入lua
                try:
                    float(dictTmp[key1][key2])
                except ValueError:
                    out.write("\t\t%s = '%s',\n" % (key2, dictTmp[key1][key2]))
                else:
                    out.write('\t\t%s = %s,\n' % (key2, dictTmp[key1][key2]))
            else:
                out.write('\t\t%s = {\n' % str(key2))
                for key3 in range(len(dictTmp[key1][key2])):
                    if type(dictTmp[key1][key2][key3]) != list:
                        try:
                            float(dictTmp[key1][key2][key3])
                        except ValueError:
                            out.write("\t\t\t[%s] = '%s',\n" % (key3+1, dictTmp[key1][key2][key3]))
                        else:
                            out.write('\t\t\t[%s] = %s,\n' % (key3+1, dictTmp[key1][key2][key3]))
                    else:
                        out.write('\t\t\t[%s] = {\n' %(key3+1))
                        for key4 in dictTmp[key1][key2][key3]:
                            try:
                                float(key4)
                            except ValueError:
                                out.write("\t\t\t\t'%s',\n" % key4)
                            else:
                                out.write('\t\t\t\t%s,\n' % key4)
                        out.write('\t\t\t},\n')
                out.write('\t\t},\n')

        out.write('\t},\n')
    out.write('}\n')
    out.close()

# sqlite里面的表转换成lua
def table2Lua(tableName):
    dictTmp = generateDict(tableName)
    writeDict2Lua(dictTmp, tableName)

if __name__ == "__main__":
    filePathDict = getFilePathDict()

    db = sqlite3.connect('VALUE_DB.db')
    cur = db.cursor()

    # table2Lua("item_base")
    # 表名
    names = cur.execute("select name from sqlite_master where type = 'table' order by name").fetchall()
    for i in names:
        if i != names[0]:
            print(i)
            table2Lua(i)

    cur.close()