date;
date -s '23:59:58';

while true
do
second=`date '+%S'`
date '+%r'
if [ $second -eq 0 ]
then
	sleep 3
	date
	date -s '+14min + 50 second' +"%r"
fi
sleep 1
done
