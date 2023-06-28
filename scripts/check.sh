cd /home/darren/git/pyfi-private || exit
date >/tmp/deploy
docker images|grep -v develop|awk '{ print "docker rmi "$3 }'|sh
make deploy >> /tmp/deploy 2>&1
