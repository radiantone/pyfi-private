cd /home/ubuntu/git/pyfi-private || exit
git pull --force
date >/tmp/deploy
make deploy >> /tmp/deploy 2>&1
