from django.db import models
import requests
from bs4 import BeautifulSoup
import json
import re

# Create your models here.
class ZiroomController:
    def __init__(self):
        self.__room_list = []

    def GetRoomList(self):
        return __room_list

    def ClearRoomList(self):
        self.__room_list = []
    
    def QueryRoomsByAddr(self, address='', price_min='0', price_max='99999', page=1, limit=1000):
        url = 'http://www.ziroom.com/z/nl/'
        url += 'r%sTO%s' % (price_min, price_max)
        url += '-z2.html'
        headers = {
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Connection':'keep-alive',
            'Host':'www.ziroom.com',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0',
            'X-Requested-With':'XMLHttpRequest'
        }
        params = {
            'qwd':address,
            'p':page,
        }
        geturl = ''.join([key + '=' + str(val) + '&' for key, val in params.items()])
        if geturl[-1] is '&':
            geturl = geturl[:-1]
        r = requests.get(url, headers=headers, params=params)
        soup = BeautifulSoup(r.text,'lxml')
        result = []
        if not soup.find('div', class_='nomsg area') is None:
            return result
        page_max = 1
        if not soup.find('div', id='page') is None and not soup.find('div', id='page').find('span') is None:
            page_max = re.search('\d+', soup.find('div', id='page').find('span', class_=False).text).group()
        t1a = soup.find_all('a', class_='t1')
        for item in t1a:
            room = Room(item['href'], address)
            result.append(room.__dict__)
            self.__room_list.append(room)
            if page*18 > limit:
                return result
        if page <= int(page_max):
            result += self.QueryRoomsByAddr(address=address, price_min=price_min, price_max=price_max, page=page+1, limit=limit-len(result))

        return result

    def QueryRoomsByBus(self, busline='', price_min='0', price_max='99999', limit=100):
        self.busline = Busline(busline)
        result = []
        for line in self.busline.bussite:
            LenBefore = len(result)
            result += self.QueryRoomsByAddr(address=line, price_min=price_min, price_max=price_max, limit=limit)
        return result

class Room:
    def __init__(self, url, keyword=''):
        self.url = 'http:' + url
        self.keyword = keyword

        self.GetRoomInfo()
        self.GetPrice()
    
    def GetRoomInfo(self):
        headers = {
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Connection':'keep-alive',
            'Host':'www.ziroom.com',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0',
            'X-Requested-With':'XMLHttpRequest'
        }
        self.traffic = {}
        r = requests.get(self.url, headers=headers)
        self.cookies = r.cookies.get_dict()
        soup = BeautifulSoup(r.text,'lxml')
        self.houseId = soup.find('input', id='house_id')['value']
        self.roomId = soup.find('input', id='room_id')['value']
        self.roomName = soup.find('div', class_='room_name').find('h2').text.strip()
        self.linelist = []
        if not soup.find('span', id='lineList') is None:
            linelist = soup.find('span', id='lineList').text.strip().split('\n')
            self.linelist = [x for x in linelist if '' != x.strip()]
        for abr in soup.find_all('strong'):
            self.traffic[abr.text] = abr.nextSibling
        self.PayWay = soup.find('span', class_='price').find('span', class_='gray-6').text

    def GetPrice(self):
        from public.test import GetVerifyByImg
        headers = {
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Connection':'keep-alive',
            'Host':'www.ziroom.com',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0',
            'X-Requested-With':'XMLHttpRequest'
        }
        params = {
            'id' : self.roomId,
            'house_id' : self.houseId,
        }
        r = requests.get('http://www.ziroom.com/detail/info', headers=headers, params=params, cookies=self.cookies)
        price_data = r.json()['data']['price']
        price_index = price_data[-1]
        AuthCode = GetVerifyByImg('http:' + price_data[0])
        price = ''
        for i in price_index:
            price += AuthCode[int(i)]
        self.price = price
        from public.LogHelper import logger
        logger().warning('http:' + price_data[0] + '\t' + ''.join(str(n) for n in price_index) + '\t' + AuthCode + '\t' + price)
        
class Busline:
    def __init__(self, line):
        self.bussite = []

        if line.isdigit():
            line += '路'
        self.busline = line
        self.GetBussite()

    def GetBussite(self):
        headers = {
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Connection':'keep-alive',
            'Host':'beijing.8684.cn',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0'
        }
        params = {
            'k':'pp',
            'q':self.busline,
        }
        r = requests.get('http://beijing.8684.cn/so.php', headers=headers, params=params)
        if r.text is None:
            exit()
        soup = BeautifulSoup(r.text, 'lxml')
        buslinesite = soup.findAll(class_='bus_line_site')
        if len(buslinesite)>0:
            siteinfo = buslinesite[0].find_all('a')
            for item in siteinfo:
                self.bussite.append(item.string)
