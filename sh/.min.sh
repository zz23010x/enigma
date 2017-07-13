echo "start ..."
echo "press Ctrl + C stop"
echo > result.txt

while ((1))
do
	hour=`date '+%H'`
	date -s $hour':59:45'
	sleep 30

	hour2=`date '+%H'`
	date -s $hour2':14:45'
	sleep 30

	date -s $hour2':29:45'
	sleep 30

	date -s $hour2':44:45'
	sleep 30

	date '+%r' >> result.txt
	echo "core文件个数" >> result.txt
	ls /server/TheThreeKingdoms2/beta/gameserver_beta/ | grep core  >> result.txt
	ls /server/TheThreeKingdoms2/beta/gameserver_beta/ | grep core | wc -l >> result.txt
	echo "cache文件个数" >> result.txt
	ls /server/TheThreeKingdoms2/beta/gameserver_beta/log | grep cache | wc -l >> result.txt
done