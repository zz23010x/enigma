from selenium import webdriver
from bs4 import BeautifulSoup
import os
import requests 
import re
from PIL import Image
import pytesseract
from io import BytesIO

def testFirefox():
    browser = webdriver.Firefox()
    browser.get("https://www.baidu.com")

def testzr():
    url = 'http://www.ziroom.com/z/nl/r2'
    url += '-r2000TO3000'
    url += '.html'
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
        'qwd':'北苑'
    }
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text,'lxml')
    a = soup.find_all('a', class_='t1')
    print(len(a))
    for i in a:
        print(i.string + i['href'])
    ra = Room(a[0]['href'])
    
def testbus():
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
        'q':'345路',
    }
    r = requests.get('http://beijing.8684.cn/so.php', headers=headers, params=params)
    soup = BeautifulSoup(r.text, 'lxml')
    a = soup.findAll(class_='bus_line_site')
    if len(a)>0:
        b = a[0].find_all('a')
        for i in b:
            print(i.string)
    print(b)
    # # resp.text返回的是Unicode型的数据。
    # # resp.content返回的是bytes型也就是二进制的数据。
    # r.encoding = 'utf-8'
    # a = r.text
    # # pattern = re.compile('bus_line_site.*?</div></div></div>')
    # pattern2 = re.compile(' >.*?</a>')
    # pattern3 = re.compile('(?<=\>).*?(?=\<)')
    # b = re.search('bus_line_site.*?</div></div></div>', a)
    # c = re.findall(pattern2, b.group())
    # print(str(c))
    # d = re.findall(u'[\u4e00-\u9fff]+', str(c))
    # print(d)
    # with open('aaa.html','w',encoding='utf-8') as f:
    #     f.write(b.group())

def ImageToString(img, num=0):
    #对于识别成字母的 采用该表进行修正  
    rep={
        ' ':'',
        'O':'0',
        'Q':'0',
        'I':'1',
        'L':'1',  
        'Z':'2',  
        '/':'7',
        '{':'7',
        'S':'8',
    }
    __standard_resolution = [(1440,220),(1640,240),(1800,230),(1920,280),(1970,230),(2160,330),(2200,310),(2440,320),(2550,360),(2900,410)]
    after_img = img.resize(__standard_resolution[num])
    #识别  
    text = pytesseract.image_to_string(after_img)  
    #识别对吗  
    text = text.strip()  
    text = text.upper()
    for r in rep:  
        text = text.replace(r,rep[r])   
    #out.save(text+'.jpg')
    result = False
    if len(text) is 10:
        result = True
    if result:
        for i in range(0,10):
            if not str(i) in text:
                result = False
    if not result and num == 9:
        text = '1234567890'
        result = True
        logger().error('[image to string failed]-[{0}]-[{1}]'.format(path, text))

    return text, result

def GetVerifyByImg(path):
    if 'http://' in path:
        res = requests.get(path)
        bPath = BytesIO(res.content)

    # 二值化  
    threshold = 140  
    table = []  
    for i in range(256):  
        if i < threshold:  
            table.append(0)  
        else:  
            table.append(1)  
    #打开图片  
    im = Image.open(bPath)  
    #转化到灰度图
    imgry = im.convert('L')
    #保存图像
    # imgry.save('g'+name)  
    #二值化，采用阈值分割法，threshold为分割点 
    out = imgry.point(table,'1')  
    # out.save('b'+name)
    height, width = out.size
    for i in range(0, 10):
        text, isNum = ImageToString(out, i)
        if isNum:
            break
        from public.LogHelper import logger
        logger().warning('[image to string failed]-[{0}]-[{1}:\t{2}]'.format(path, str(i+1), text))

    return text  

def RetrievalControl(soup, contype, word):
    result = []
    result1 = soup.find_all('div')
    for i in result1:
        if len(i.find_all(contype))>0:
            for j in i.find_all(contype):
                try:
                    if word in j.text:
                        result.append(j)
                except:
                    pass
    return result

def str_to_int(str, i=0):
    try:
        result = int(str.strip())
    except:
        result = i
    finally:
        return result

if __name__ == '__main__':
    print(123)