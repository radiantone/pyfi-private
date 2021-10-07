docker ps -a|grep -v CONTAINER|awk '{ print "docker stop "$1}'|sh
docker ps -a|grep -v CONTAINER|awk '{ print "docker rm "$1}'|sh
