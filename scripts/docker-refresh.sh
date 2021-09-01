docker ps -a|awk '{ print "docker stop "$1}'|sh
docker ps -a|awk '{ print "docker rm "$1}'|sh
