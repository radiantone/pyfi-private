cd /home/darren/git/pyfi-private
date >/tmp/deploy
make refresh
make deploy >> /tmp/deploy 2>&1
