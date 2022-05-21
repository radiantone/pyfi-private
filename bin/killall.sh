ps -ef|grep celery|grep -v grep|awk '{ print "kill -9 "$2}'|sh
ps -ef|grep pyfi|grep -v grep|awk '{ print "kill -9 "$2}'|sh
