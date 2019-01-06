'''REM /P 删除每一个文件之前提示确认。
REM /F 强制删除只读文件。
REM /S 从所有子目录删除指定文件。
REM /Q 安静模式。删除全局通配符时，不要求确认。
REM /A 根据属性选择要删除的文件。 

del /s /q %~dp0Logs\*.log'''

import os

for dir in os.listdir(os.path.join(os.getcwd(), 'Logs')):
    if dir.endswith('.log'):
        os.remove(os.path.join(os.path.join(os.getcwd(), 'Logs/', dir)))