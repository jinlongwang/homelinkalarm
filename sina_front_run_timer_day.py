#coding=utf-8
import threading, time, Queue
import  DButil
import urllib2
import re
import socket
from logger import *
from bs4 import BeautifulSoup
import sys

socket.setdefaulttimeout(10)
reload(sys)
sys.setdefaultencoding('utf8')
base_url_head = 'http://bj.esf.sina.com.cn/house/'
THREAD_LIMIT = 15
jobs = Queue.Queue(0) # arg1 means "No item limit"
rss_to_process = Queue.Queue(THREAD_LIMIT) # We set a limit on this, I'll
# explain later
def thread():
    while True: # forever
        try:
            feed_url = jobs.get(False) # arg1 means "Don't wait for items
            # to appear"
        except Queue.Empty:
            # Nothing left to do, time to die
            return
        timeline = getTimeLine()
        getDataFromUrl(feed_url,timeline)
# queue is too large
def getWebPageContent(url):
    try:
        print 'wating for open url'
        headers = {
            'Referer':'http://bj.esf.sina.com.cn/house/'
        }
        req = urllib2.Request(
            url = url,
            headers = headers )
        f = urllib2.urlopen(req)
        print  'wating for read'
        #t = Timer(20, f.close)
        #t.start()
        data = f.read()
        f.close()
        print  'finish read'
        return data
    except Exception,e :
        print 'open url error',e
        return ''

def getWebCount(area_):
    #url = 'http://bj.esf.sina.com.cn/house/o国美第一城'
    url = base_url_head +'o'+ area_
    url = url.encode('utf-8')
    print  url
    content = getWebPageContent(url).decode('GB2312','ignore').encode('UTF-8')
    #print  content.decode('gbk')
    #content = content.decode('gbk')
    try:
        category = re.compile(r'<div class="search_bottom_page_num">(.*?)<div class="clear"></div>',re.DOTALL).findall(content)[0]
        #print  category
        url_tail = re.compile(r'<a href="/house/(.*?)/"',re.DOTALL).findall(category)[0]
        tail = url_tail.split('-')[0]
        #print  url_tail
        page_count = re.compile(r'<span class="all">(.*?)</span>',re.DOTALL).findall(category)[0]
        #print page_count[1:-1]
    except :
        tail = ''
        page_count = ''
    #print tail,page_count,'-----------------------'
    return tail,page_count

def  getDataFromUrl(area,timeline):
    #url_tail,page_count = getWebCount(area)
    getInfo(area,timeline)

def getInfo(area,timeline):
    #print count,tail,'.........................'
    #if count == '':
    #    return
    #if count > 3:
    #    count = 3
    number = 0
    #for i in range(int(count)):
    url = base_url_head +'o'+ area
    print  url,'uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu'
    content = getWebPageContent(url).decode('GB2312','ignore').encode('UTF-8')
    innerContent = re.compile(r'<div class="search_item_list">(.*?)<!--search_item_list -->',re.DOTALL).findall(content)[0]
    #print  category[0]
    soup = BeautifulSoup(innerContent, from_encoding="utf-8")
    category = soup.find_all("div", class_="inventory_list_house inventory_out _houselist")
    print len(category)
    infoList = []
    for cate in category:
        v_flag = 0
        number += 1
        try:
            title =  cate.find_all('a', class_='hs')[0].string
            print title
        except Exception,e:
            print e
            title = ""

        try:
            brokerName = cate.find_all('div', class_='inventory_list_r_agent')[0].contents[1].string
            print brokerName
        except Exception, e:
            print e
            brokerName = ""

        try:
            houseType = cate.find_all('span', class_='widthspanone')[0].string
            print houseType
        except Exception, e:
            print e
            houseType = ""

        try:
            size = cate.find_all('span', class_='widthspantwo')[0].string
            print size
        except Exception, e:
            print e
            size = ""

        try:
            amount = cate.find_all('div', class_='inventory_list_r_name_price')[0].contents[0]
            print amount
        except Exception, e:
            amount = ""

        try:
            company = cate.find_all('div', class_='inventory_list_r_company')[0]
            if len(company['class']) > 1:
                v_flag = 1
            else:
                v_flag = 0
            company = company.contents
            company = company[0] if len(company)==1 else company[1]
            company = company.string
            print company
        except Exception, e:
            print e
            company = checkCompany(title)

        dit = {'HOUSENAME':area,
               'TITLE':title,
               'CROP':company,
               #'SHOP':shop,
               'TOTAL_AMOUNT':amount,
               'SIZE':size,
               'HOUSE_TYPE':houseType,
               #'LOCATION':address,
               'IS_BID':v_flag,
               'SOURCE':'sina',
                'BROKER_NAME':brokerName,
               'URL':"",
               'EXT2':number,
               'EXT1':"",
               'EXT3':timeline}
        infoList.append(dit)
    print  'sssssssssssssssss'
    print 'put to the out queue ...........................'
    DButil.insertHouse(infoList)
    time.sleep(2)

def main():
    for info in DButil.selectArea(): # Load them up
        jobs.put(info)

    for n in xrange(THREAD_LIMIT): # Unleash the hounds
        t = threading.Thread(target=thread)
        t.start()

def timer():
    while True:
        #if there is a exception, this try-catch will reset the jobs,and wait for next turn
        try:
            time_  =  time.strftime('%H',time.localtime(time.time()))
            minute =  time.strftime('%M',time.localtime(time.time()))
            print  int(time_),int(minute),'========='
            if  7 <= int(time_) <= 23:
                if int(minute) == 0:
                #if int(minute) == 30:
                    print  'start============'
                    main()
                    #AppLogger.log('run thread over')
                    time.sleep(60)
                else:
                    print 'wrong minute========='
                    time.sleep(60)
            else:
                print 'wrong time'
                #AppLogger.log('wrong time')
                time.sleep(60)
        except Exception,e:
            print  e
            AppLogger.log('timer() is crash'+":"+str(e))
            jobs.queue.clear()
            time.sleep(60)

def getTimeLine():
    timeline  =  time.strftime('%Y-%m-%d %H',time.localtime(time.time()))
    time_  =  time.strftime('%H',time.localtime(time.time()))
    minute =  time.strftime('%M',time.localtime(time.time()))
    print  minute
    return timeline+":00"

def checkCompany(title):
    company = "no"
    companyList = ["链家", "中天", "我爱我家", "麦田"]
    for c in companyList:
        if title.find(c) > -1:
            company = c
            break
    return company

if __name__ == "__main__":
    AppLogger.log("start!")
    timer()
    #main()

