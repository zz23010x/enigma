echo "start ..."
echo "press Ctrl + C stop"

url=`pwd`
gpid=`cat gameserver_beta/pid`
dpid=`cat dbiserver_beta/pid`
lscpu > result.txt
free -m >> result.txt
echo 游戏服进程:$gpid
echo DB服进程:$dpid
echo >> result.txt
while ((1))
do
	LC_ALL=zh_CN.UTF-8 date >> result.txt
	echo "在线人数" >> result.txt
	netstat -nat|grep -i 4012|wc -l >> result.txt
	echo "cache文件个数" >> result.txt
	ls $url/gameserver_beta/config |grep cache|wc -l >> result.txt
	#echo "root  进程号  CPU占用  内存占用  使用虚拟内存  占用固定内存" >> result.txt
	#ps aux | grep $url >> result.txt
	top -p $gpid -n 1 | grep -E "server|PID" >> result.txt
	top -p $dpid -n 1 | grep -E "server" >> result.txt
	#top -p $gpid -n 1 | awk '/server/{print "游戏服占用CPU百分比:"$9"%";print "游戏服占用物理内存百分比:"$10"%"}' >> result.txt
	#top -p $dpid -n 1 | awk '/server/{print "DB服占用CPU百分比:"$10"%";print "DB服占用物理内存百分比:"$11"%"}' >> result.txt
	echo "游戏服日志" >> result.txt
	newfile=''
	for i in `ls -tr $url/gameserver_beta/log`
	do
		newfile=$i;
	done

	awk '/statistic/{a=$0}END{print a}' $url/gameserver_beta/log/$newfile >> result.txt
	echo 	file:$newfile >> result.txt
	echo "	atps: 每秒accept的连接数(transfer)
	ctps: 每秒connect的连接数(transfer)
	dtps: 每秒销毁的连接数(transfer)
	ccps: 每秒创建的上下文数(流程context)
	dcps: 每秒销毁的上下文数(流程context)
	rmps: 每秒recv的完整消息(message)
	smps: 每秒send的完整消息(message)
	rbps:  每秒recv的字节数(bytes)
	sbps:  每秒send的字节数(bytes)
	aliveT: 当前存活的连接数(transfer)
	aliveC: 当前存活的上下文数(流程context)
	Wait:队列里等待处理的任务数（）" >> result.txt
	iostat -d >> result.txt
	echo "硬盘设备  每秒的传输次数  读取数据量/秒  写入数据量/秒  读取总数据量  写入总数据量" >> result.txt
	echo >> result.txt

	sleep 20
done
