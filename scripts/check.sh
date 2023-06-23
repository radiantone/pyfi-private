cd /home/darren/git/pyfi-private
date >/tmp/deploy
docker images|grep -v local|awk '{ print "docker rmi "$3 }'|sh
make deploy >> /tmp/deploy 2>&1
