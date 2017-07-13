import os, sys
import urllib.parse
import urllib.request

url = 'http://192.168.12.34:8888/Other/Signin'
values = {
    'account': os.path.basename(__file__).split(".")[0]
}
data = urllib.parse.urlencode(values)
# that params output from urlencode is encoded to bytes before it is sent to urlopen as data  
data = data.encode('utf-8')
req = urllib.request.Request(url, data)
response = urllib.request.urlopen(req)

html = response.read()
print(html.decode('utf-8'))
print("签到后勿忘指纹打卡")
print("此窗口直点x关闭")
while 1:
	pass