# -*- coding: utf-8 -*-
import MySQLdb
import os,sys
import ConfigParser
cf = ConfigParser.ConfigParser()
cf.read("db.conf")
database = cf.get("DB", "DATABASE")
hostname = cf.get("DB", "HOSTNAME")
port     = cf.get("DB", "PORT")
uid      = cf.get("DB", "UID")
pwd      = cf.get("DB", "PWD")

def insertArea(param):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    conn = MySQLdb.connect(host=hostname, user=uid,db=database,passwd=pwd,port=int(port),use_unicode=True,charset="utf8")
    cursor = conn.cursor()
    for t in param:
        try:
            sql="insert into tbhouse_list(HOUSE_NAME,AREA,BOARD,SOURCE) values ('"+t['housename']+"','"+t['area']+"','"+t['board']+"','anjuke')"
            cursor.execute(sql)
            conn.commit()
        except Exception,e:
            print e
            continue
    conn.close()

def selectBoard():
    conn = MySQLdb.connect(host=hostname, user=uid,db=database,passwd=pwd,port=int(port),use_unicode=True,charset="utf8")
    arealist = []
    cursor = conn.cursor()
    sql = 'SELECT AREA, BOARD,SPELL,AREA_SPELL FROM tbhouse_board'
    cursor.execute(sql)
    results = cursor.fetchall()
    print len(results),'*******'
    for r in results:
        dit = {'name':r[0]+'-'+r[1],
               'url_tail':r[3]+'/'+r[2]}
        arealist.append(dit)
    conn.close()
    return arealist


def insertBoard(param):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    conn = MySQLdb.connect(host=hostname, user=uid,db=database,passwd=pwd,port=int(port),use_unicode=True,charset="utf8")
    cursor = conn.cursor()
    for t in param:
        try:
            sql="insert into tbhouse_board(AREA,BOARD,SPELL) values ('"+t['area']+"','"+t['name']+"','"+t['spell']+"')"
            cursor.execute(sql)
            conn.commit()
        except:
            print 'already had this house!!!'
            continue
    conn.close()

def selectArea():
    print hostname,uid
    conn = MySQLdb.connect(host=hostname, user=uid,db=database,passwd=pwd,port=int(port),use_unicode=True,charset="utf8")
    arealist = []
    cursor = conn.cursor()
    sql = 'select HOUSE_NAME from ganji_list'
    cursor.execute(sql)
    results = cursor.fetchall()
    print len(results),'*******'
    for r in results:
        #print  r[0]
        arealist.append(r[0])
    conn.close()
    return arealist


def insertHouse(param):
    conn = MySQLdb.connect(host=hostname, user=uid,db=database,passwd=pwd,port=int(port),use_unicode=True,charset="utf8")

    reload(sys)
    sys.setdefaultencoding('utf-8')
    cursor = conn.cursor()
    for t in param:
        try:
            print str(t['TITLE'])
            #sql = "insert into tbhouse_data(HOUSE_NAME,CROP,SHOP,TOTAL_AMOUNT,SIZE,HOUSE_TYPE,IS_BID,BROKER_NAME,URL,EXT2,EXT3) values ('" + str(
            #    t['HOUSENAME']) + "' ,'" + str(t['CROP']) + "','" + str(
            #    t['SHOP']) + "','" + str(t['TOTAL_AMOUNT']) + "','" + str(t['SIZE']) + "','" + str(
            #    t['HOUSE_TYPE']) + "','" + str(t['IS_BID']) + "',,'"+t['BROKER_NAME']+"','"+t['URL']+"','"+str(t['EXT2'])+"','"+t['EXT3']+"')"
            sql = "insert into tbhouse_data_sina_day(HOUSE_NAME,CROP,IS_BID,URL,EXT2,EXT3,TITLE,SOURCE,TOTAL_AMOUNT,SIZE,HOUSE_TYPE,BROKER_NAME,EXT1) values ('" + str(
                t['HOUSENAME']) + "' ,'"+t['CROP']+"','" + str(t['IS_BID']) + "','"+t['URL']+"','"+str(t['EXT2'])+"','"+t['EXT3']+"','"+t['TITLE']+"','"+t['SOURCE']+"','"+t['TOTAL_AMOUNT']+"','"+t['SIZE']+"','"+t['HOUSE_TYPE']+"','"+t['BROKER_NAME']+"','"+t['EXT1']+"')"
            #sql="insert into tbhouse_list(HOUSE_NAME,AREA,ADDRESS) values ('你妈','接口','佛挡杀佛')"
            #sql="insert into tbhouse_data(HOUSE_NAME,TITLE,CROP,SHOP,TOTAL_AMOUNT,SIZE,HOUSE_TYPE,LOCATION,IS_BID,EXT1) values ('10AM新坐标','b','c','d','11','12','f','f','1','s')"

            cursor.execute(sql)
            conn.commit()
        except Exception,e:
            print e,'error++++++++++++++++++++'
            continue
    conn.close()

def insert_anjuke_backinfo(param):
    conn = MySQLdb.connect(host=hostname, user=uid,db=database,passwd=pwd,port=int(port),use_unicode=True,charset="utf8")

    reload(sys)
    sys.setdefaultencoding('utf-8')
    cursor = conn.cursor()
    for t in param:
        try:
            sql = "insert into tbanjuke_back_data(HOUSE_ID,CLICK_COUNT,CREATE_TIME,USER_NAME,AMOUNT)values('"+str(t['HOUSE_ID'])+"','"+str(t['CLICK_COUNT'])+"',sysdate(),'"+str(t['USER_NAME'])+"','"+str(t['AMOUNT'])+"');"
           
            cursor.execute(sql)
            conn.commit()
        except Exception,e:
            print e,'error++++++++++++++++++++'
            continue
    conn.close()

if __name__ == "__main__":
    a = selectBoard()
    for i  in a:
        print i['name']
      
      
