import os
from appium import webdriver
from selenium.common.exceptions import NoSuchElementException
import subprocess
import time

class AppDevice:
    def __init__(self, appPackage, appActivity):
        self.desired_caps = {}
        self.desired_caps['platformName'] = 'Android'
        self.desired_caps['appPackage'] = appPackage
        self.desired_caps['appActivity'] = appActivity
        self.GetDevices()
        self.GetDeviceVersion()

    def GetDeviceVersion(self):
        self.desired_caps['platformVersion'] = os.popen('adb shell getprop ro.build.version.release').read().strip()

    def SetDevices(self, devicename):
        self.desired_caps['deviceName'] = devicename

    def GetDevices(self):
        DevicesArr = []
        for num, dev in enumerate(os.popen('adb devices').read().strip().splitlines()):
            if num > 0:
                DevicesArr.append(dev.split('\t')[0])
        if DevicesArr != []:
            self.SetDevices(DevicesArr[0])
        return DevicesArr

    def StartApp(self):
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', self.desired_caps)
        self.getSize()

    def getSize(self):                               #获取当前的width和height的x、y的值
        self.width = self.driver.get_window_size()['width']   #width为x坐标
        self.height = self.driver.get_window_size()['height']  #height为y坐标

    def swipeUp(self):  #当前向上滑动swipeup
        x1 = int(self.width * 0.5)  
        y1 = int(self.height * 0.75)   
        y2 = int(self.height * 0.25)   
        self.driver.swipe(x1, y1, x1, y2,500)  #设置时间为500

    def swipLeft(self):      #当前向左进行滑动swipleft
        x1=int(self.width*0.75)
        y1=int(self.height*0.5)
        x2=int(self.width*0.05)
        self.driver.swipe(x1,y1,x2,y1,500)

    def swipeDown(self):    #向下滑动swipedown
        x1 = int(self.width * 0.5)
        y1 = int(self.height * 0.25)
        y2 = int(self.height * 0.75)
        self.driver.swipe(x1, y1, x1, y2,500)

    def swipRight(self): #向右滑行swipright
        x1=int(self.width*0.05)
        y1=int(self.height*0.5)
        x2=int(self.width*0.75)
        self.driver.swipe(x1,y1,x2,y1,500)

    def touch_tap(self,x,y,duration=100):   #点击坐标  ,x1,x2,y1,y2,duration
            screen_width = self.driver.get_window_size()['width']  #获取当前屏幕的宽
            screen_height = self.driver.get_window_size()['height']   #获取当前屏幕的高
            a =(float(x)/screen_width)*screen_width
            x1 = int(a)
            b = (float(y)/screen_height)*screen_height
            y1 = int(b)
            self.driver.tap([(x1,y1),(x1,y1)],duration)

    def ExitApp(self):
        self.driver.quit()
    
    def keyboard_input(self, str):
        subprocess.Popen('adb -s %s shell input text %s' % (self.desired_caps['deviceName'], str))

    def isElement(self, identifyBy, c):
        '''
        Determine whether elements exist
        Usage:
        isElement(By.XPATH,"//a")
        '''
        flag=None
        try:
            if identifyBy == "id":
                #self.driver.implicitly_wzait(60)
                self.driver.find_element_by_id(c)
            elif identifyBy == "xpath":
                #self.driver.implicitly_wait(60)
                self.driver.find_element_by_xpath(c)
            elif identifyBy == "class":
                self.driver.find_element_by_class_name(c)
            elif identifyBy == "link text":
                self.driver.find_element_by_link_text(c)
            elif identifyBy == "partial link text":
                self.driver.find_element_by_partial_link_text(c)
            elif identifyBy == "name":
                self.driver.find_element_by_name(c)
            elif identifyBy == "tag name":
                self.driver.find_element_by_tag_name(c)
            elif identifyBy == "css selector":
                self.driver.find_element_by_css_selector(c)
            flag = True
        except NoSuchElementException as e:
            flag = False
        except Exception as e:
            print(e)
        finally:
            return flag

    def claer_cache(self):
        subprocess.Popen('adb shell pm clear %s' % (self.desired_caps['appPackage']))

def GetFocusedActivity(t=3):
    for i in range(t):
        print(subprocess.Popen('adb shell dumpsys activity| findstr mFocusedActivity', shell=True, stdin=subprocess.PIPE))
        time.sleep(1)