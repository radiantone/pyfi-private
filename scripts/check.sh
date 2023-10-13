cd /home/darren/git/pyfi-private || exit
date >/tmp/deploy
make deploy >> /tmp/deploy 2>&1
