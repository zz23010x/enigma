from django.db import models
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode
import json
from copy import deepcopy
import time
import random

# Create your models here.
class JobzhilianController:
    def __init__(self):
        self.__job_list = []
        self.__historical_records = {}
        self.__db_name = 'tab_job_info_zhilian'
        self.__keyword = None

    def QueryJobsByPosition(self, position='', money_interval='15000,25000', page=1, limit=1000):
        url = 'https://fe-api.zhaopin.com/c/i/sou'
        headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0',
        }
        params = {
            'kw':position,
            'cityId':530,
            'salary': money_interval,
            'kt':3,
            'et':2,
            'pageSize':100,
            'start':page
        }
        already_startpage = self.GetJobCache(params)
        if already_startpage <= page or len(self.__job_list) < limit:
            params['start'] = already_startpage
            r = requests.get(url, headers=headers, params=params)
            num = r.json()['data']['numFound']
            res = r.json()['data']['results']
            for item in res:
                job = Job()
                if job.InitJobInfo(item):
                    self.__job_list.append(job)
            self.SaveJobCache(params)
            # self.WriteToDB(position)
            if len(self.__job_list) >= limit:
                return len(self.__job_list)
            if page + 100 <= num:
                self.QueryJobsByPosition(position=position, money_interval=money_interval, page=page+100, limit=limit)

        return len(self.__job_list)

    def UpdateJobsInfo(self, position='', page=1):
        from public.sqlite3Helper import DataBaseServer
        from public.LogHelper import logger
        self.ClearJoblist()
        self.QueryJobsByPosition(position=position)
        DataBaseServer().DropAllTables()
        self.WriteToDB(position)
        logger().info('[JobsInfo Update Success]-[0]-[1]'.format(position, len(self.__job_list)))

    def ClearJoblist(self, key=None):
        if not key is None and key == self.__keyword:
            return False
        self.__job_list.clear()
        return True

    def SaveJobCache(self, params):
        if not params['kw'] in self.__historical_records:
            self.__historical_records[params['kw']] = [{'params':params, 'jobs': deepcopy(self.__job_list)}]
        else:
            for item_para in self.__historical_records[params['kw']]:
                if item_para['params']['salary'] == params['salary'] and item_para['params']['start'] < params['start']:
                    item_para['jobs'] += deepcopy(self.__job_list)
                    return True
            self.__historical_records[params['kw']].append({'params':params, 'jobs': deepcopy(self.__job_list)})

    def GetJobCache(self, params):
        if params['kw'] in self.__historical_records:
            for item_para in self.__historical_records[params['kw']]:
                if item_para['params']['salary'] == params['salary']:
                    self.__job_list = deepcopy(item_para['jobs'])
                    return item_para['params']['start']+100

        return params['start']

    def ListToJson(self, list, count=0):
        result = []
        if count == 0 or count > len(self.__job_list):
            for item in self.__job_list:
                result.append(item.__dict__)
        else:
            for item in self.__job_list[:count]:
                result.append(item.__dict__)
        return json.dumps(result)

    def WriteToDB(self, key):
        from public.sqlite3Helper import DataBaseServer
        params = []
        maxId = DataBaseServer().SelectTable('select max(id) from tab_job_info_zhilian')
        if maxId[0][0] is None:
            index_id = 0
        else:
            index_id = maxId[0][0]
        for item in self.__job_list:
            index_id += 1
            params.append((index_id, item.ID, str(item.__dict__), key))
        DataBaseServer().InsertValues('replace into tab_job_info_zhilian values(?,?,?,?)', params)

    def ReadFromDB(self, key):
        from public.sqlite3Helper import DataBaseServer
        result = []
        datas = DataBaseServer().SelectTable('select * from tab_job_info_zhilian where keyword like "%{0}%"'.format(key))
        for item in datas:
            loadJob = Job()
            loadJob.LoadFromDict(eval(item[2]))
            self.__job_list.append(loadJob)
            result.append(item[1])
        self.__keyword = key
        return result

    def FilterData(self, position='', money_interval='1,2'):
        result = []
        money_min = float(money_interval.split(',')[0])
        money_max = float(money_interval.split(',')[1])
        for item in self.__job_list:
            print(item.moneyMin >= money_min, item.moneyMax <= money_max, money_min, money_max, item.moneyMin, item.moneyMax)
            if item.moneyMin >= money_min and item.moneyMax <= money_max:
                result.append(item)
        return result

    def GetCountMax(self, position='', money_interval=''):
        from public.CacheHelper import GetCacheByListRandom
        url = 'https://fe-api.zhaopin.com/c/i/sou'
        params = {
            'kw':position,
            'cityId':530,
            'salary': money_interval,
            'kt':3,
            'et':2,
            'pageSize':100,
            'start':1
        }
        r = requests.get(url, headers=GetCacheByListRandom('cache_user_agent'), params=params)
        return r.json()['data']['numFound']
    
    def aaa(self, position='', money_interval='', page='1'):
        from public.CacheHelper import GetCacheByListRandom
        url = 'https://fe-api.zhaopin.com/c/i/sou'
        params = {
            'kw':position,
            'cityId':530,
            'salary': money_interval,
            'kt':3,
            'et':2,
            'pageSize':100,
            'start':page
        }
        time.sleep(random.random()*3)
        r = requests.get(url, headers=GetCacheByListRandom('cache_user_agent'), params=params)
        return r.json()['data']['results']

    def bbb(self, list):
        from public.ExplorerHelper import ProcessManager
        args = []
        for il in list:
            args.append((il,))
        p1 = ProcessManager()
        p1.configProcess(self.ccc, funcArgs=args, cbfuncName=self.ddd, threadNumber=10)
        p1.startProcess()

    def ccc(self, item):
        job = Job()
        if job.InitJobInfo(item):
            return job

    def ddd(self, res):
        if not res is None:
            self.__job_list.append(res)
    
    def Test(self, position='', money_interval='15000,25000', page=1, limit=1000):
        from public.ExplorerHelper import ProcessManager
        import math
        time.sleep(random.random()*3)
        maxCount = self.GetCountMax(position=position, money_interval=money_interval)
        args = []
        for i in range(int(maxCount/100)+1):
            if i==0:
                page = 1
            else:
                page = i*100
            args.append((position, money_interval, page))
        p1 = ProcessManager()
        p1.configProcess(self.aaa, funcArgs=args, cbfuncName=self.bbb, threadNumber=math.ceil(maxCount/1000))
        p1.startProcess()

class Job:
    def __init__(self):
        self.positionURL = None
        self.__blockurl = ['xiaoyuan.zhaopin.com/job']
    
    def InitJobInfo(self, data):
        self.ID = data['number']
        self.jobName = data['jobName']
        self.updateDate = data['updateDate']
        self.positionURL = data['positionURL']
        self.eduLevel = data['eduLevel']['name']
        self.company_name = data['company']['name']
        self.company_ID = data['company']['number']
        self.company_size = data['company']['size']['name']
        self.company_url = data['company']['url']
        self.salary = data['salary']
        self.welfare = ','.join(data['welfare'])
        self.city = data['city']['display']

        money_interval = data['salary'].split('-')
        if len(money_interval) == 2:
            self.moneyMin = float(money_interval[0].strip('K'))*1000
            self.moneyMax = float(money_interval[1].strip('K'))*1000

        return self.GetJobDetails()

    def GetJobDetails(self, url=''):
        from public.LogHelper import logger
        from public.CacheHelper import GetCacheByListRandom
        if not self.positionURL is None:
            url = self.positionURL
        for bkurl in self.__blockurl:
            if bkurl in url:
                logger().warning('[Block Job Url]-[{0}]'.format(url))
                return False
        time.sleep(random.random()*3)
        r = requests.get(url, headers=GetCacheByListRandom('cache_user_agent'))
        soup = BeautifulSoup(r.text,'lxml')
        try:
            jobinfos = soup.find_all('div', class_='tab-inner-cont')
            self.jobInfo = [x.text.strip() for x in jobinfos[0].find_all('p') if x.text.strip() != '']  # 职位信息
            if len(jobinfos) > 1:
                self.workInfo = jobinfos[1].text.strip()  # 公司概况
            for l in jobinfos[0].find('h2').text.strip().split('\n'):
                if not '查看公司地图' in l and l != '':
                    self.work_address = l.strip() # 工作地址
                    break

            if not soup.find('img', alt=self.company_name) is None:
                self.company_logo = soup.find('img', alt=self.company_name)['src']  # logo

            welfare = soup.find('div', class_='welfare-tab-box').find_all('span')
            if len(welfare) > 0:
                self.welfare = None
                self.welfare = ','.join([x.text for x in welfare])  # 职位福利

            for al in soup.find_all('a', attrs={'rel':'nofollow'}):
                if self.company_name in al.text:
                    self.company_url = al['href']  # 公司首页

            # a = soup.find_all('div', class_='fixed-inner-box')
            companyinfo = soup.find('ul', class_='terminal-ul clearfix terminal-company mt20')
            for lilist in companyinfo.find_all('li'):
                if '公司地址' in lilist.text:
                    for l in lilist.text.strip().split('\n'):
                        if not '公司地址' in l and not '查看公司地图' in l and l != '':
                            self.company_address = l.strip()  # 公司地址
                            break
        except Exception as e:
            logger().error('[Get Jobinfo Failed]-[{0}]-[{1}]'.format(e, str(self.__dict__)))
            return False

        return True

    def LoadFromDict(self, dictionary):
        for key in dictionary:
            setattr(self, key, dictionary[key])