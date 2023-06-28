cd /home/ubuntu/git/pyfi-private || exit
date >/tmp/deploy
make stop && make refresh && make deploy
