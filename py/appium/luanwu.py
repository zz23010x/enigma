#coding:utf-8

from appium import webdriver
import time

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '4.2'
desired_caps['deviceName'] = 'Android Emulator'
desired_caps['appPackage'] = 'com.smartspace.bladeflurry.android'
desired_caps['appActivity'] = 'main.GameActivity'

driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
time.sleep(7)

try:
	x = driver.get_window_size()['height']
	y = driver.get_window_size()['width']
	print(x,y)
	
	driver.tap([(y/2,x-270),],10)
	time.sleep(0.5)
	driver.tap([(1140,x-180),],10)
	time.sleep(0.5)

	print('press any key')
	input()
except Exception as e:
	print(e)
	driver.quit()
finally:
	print('press any key exit')
	input()
	driver.quit()

'''
appium -a 127.0.0.1 -p 4723 -U 519f849e  --no-reset

adb shell
cd system/app
cd data/app
ls | grep 'apk'

aapt dump xmltree *****.apk AndroidManifest.xml
aapt dump badging *****.apk
adb logcat -c
adb logcat ActivityManager:I *:s
'''