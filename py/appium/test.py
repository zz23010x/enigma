#coding:utf-8

import unittest
from appium import webdriver
import time

class AndroidTests(unittest.TestCase):
	def setUp(self):
		desired_caps = {}
		desired_caps['platformName'] = 'Android'
		desired_caps['platformVersion'] = '4.3'
		desired_caps['deviceName'] = 'Android Emulator'
		desired_caps['appPackage'] = 'com.smartspace.bladeflurry.android'
		desired_caps['appActivity'] = 'main.GameActivity'

		self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
		
		time.sleep(7)
		self.x = self.driver.get_window_size()['width']
		self.y = self.driver.get_window_size()['height']
		print(self.x,'x',self.y)
	
	def tearDown(self):
		self.driver.quit()
		
	def test_logoin(self):
		try:
			self.driver.tap([(self.x/2,self.y-270),],10)
			time.sleep(0.5)
			self.driver.tap([(1140,self.y-180),],10)
			time.sleep(0.5)
			self.driver.tap([(self.x/2,self.y-140),],10)
		except Exception as e:
			print(e)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(AndroidTests)
    unittest.TextTestRunner(verbosity=2).run(suite)		

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