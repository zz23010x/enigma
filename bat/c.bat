@echo off
setlocal EnableDelayedExpansion

echo 文件目录
set dbfile="C:\Users\zheng-z\Documents\My RTX Files\*.db"
echo 服务器地址
set /p url=linux ip(67,43,169,189):

echo %1|find ".db" &&copy %1 VALUE_DB.db &&goto initend

echo %1|find ".gz" &&goto server

for /f "delims=" %%a in ('dir /s/b/o-d %dbfile%') do (
	copy "%%a" VALUE_DB.db &&echo %%a &&goto initend
)
:initend

if %url% == 43 (
echo 50.43
plink.exe -pw "123456" root@192.168.50.43 find /home/tianxx/ -name gameserver1.0 -o -name teamserver1.0; cal; date;
echo 服务器路径
set /p dir=linux dir:
echo !dir!
if !dir!==date goto de43

for %%b in (!dir!) do (
start ServBty %url% VALUE_DB.db %%b
)
)

if %url% == 67 (
echo 211.67
plink.exe -pw "AoneYanfa789&*(" root@223.203.211.67 find /home/tianxx/ -name gameserver1.0 -o -name teamserver1.0; date; 
echo 服务器路径
set /p dir=linux dir:
echo !dir!
for %%b in (!dir!) do (
start ServBty %url% VALUE_DB.db %%b
)
)

if %url% == 169 (
echo 7.169
plink.exe -P 2203 -pw "AoneYanfa789&*(" yanfauser@sastest001.chinacloudapp.cn find /server/lilou -name gameserver; cal; date; 
echo 服务器路径
set /p dir=linux dir:
echo !dir!
if !dir!==date goto de169

for %%b in (!dir!) do (
start ServBty %url% VALUE_DB.db %%b
)
)

if %url% == 189 (
echo 91.189
plink.exe -i jhzr_xjp.ppk ec2-user@54.169.91.189 find /home/ec2-user -name gameserver1.0 -o -name teamserver1.0; cal; date; 
echo 服务器路径
set /p dir=linux dir:
echo !dir!
if !dir!==date goto de189

for %%b in (!dir!) do (
start ServBmy %url% VALUE_DB.db %%b
)
)

goto end

:server

if %url% == 43 (
echo 50.43
plink.exe -pw "123456" root@192.168.50.43 cd /home/tianxx/; "ls | sed s:^:`pwd`/:";
echo 服务器路径
set /p dir=linux dir:
echo !dir!
for %%b in (%*) do (
start ServBty %url% %%b !dir!
)
)

if %url% == 67 (
echo 211.67
plink.exe -pw "AoneYanfa789&*(" root@223.203.211.67 cd /home/tianxx/; "ls | sed s:^:`pwd`/:";
echo 服务器路径
set /p dir=linux dir:
echo !dir!
for %%b in (%*) do (
start ServBty %url% %%b !dir!
)
)

if %url% == 169 (
echo 7.169
plink.exe -P 2203 -pw "AoneYanfa789&*(" yanfauser@sastest001.chinacloudapp.cn cd /server/lilou/; "ls | sed s:^:`pwd`/:";
echo 服务器路径
set /p dir=linux dir:
echo !dir!
for %%b in (%*) do (
start ServBty %url% %%b !dir!
)
)

if %url% == 189 (
echo 91.189
plink.exe -i jhzr_xjp.ppk ec2-user@54.169.91.189 cd /home/ec2-user/soulsword_overseas/; "ls | sed s:^:`pwd`/:"; cd /home/ec2-user/luanwu_oversea/; "ls | sed s:^:`pwd`/:"
echo 服务器路径
set /p dir=linux dir:
echo !dir!
for %%b in (%*) do (
start ServBMy %url% %%b !dir!
)
)

goto end

:de43
set ml=pwd
set /p ml=输入命令(date -s "xxxx-xx-xx xx:xx:xx"^):
if !ml!==exit goto end
plink.exe -pw "123456" root@192.168.50.43 !ml!; date;
goto de43

:de169
set ml=pwd
set /p ml=输入命令(date -s "xxxx-xx-xx xx:xx:xx"^):
if !ml!==exit goto end
plink.exe -P 2203 -pw "AoneYanfa789&*(" yanfauser@sastest001.chinacloudapp.cn sudo !ml!; date;
goto de169

:de189
set ml=pwd
set /p ml=输入命令(date -s "xxxx-xx-xx xx:xx:xx"^):
if !ml!==exit goto end
plink.exe -i jhzr_xjp.ppk ec2-user@54.169.91.189 sudo !ml!; date;
goto de189

:end
echo 任意键退出
pause