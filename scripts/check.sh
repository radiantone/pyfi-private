CONTAINER_ID=`docker images|grep nginx|grep production|awk '{ print $3 }'`
SHA_ID=`docker inspect $CONTAINER_ID| jq .[0].Id|sed s/\"//g`
echo $SHA_ID
make login
docker compose -f docker-compose-ecr.yml pull nginx
CONTAINER_ID=`docker images|grep nginx|grep production|awk '{ print $3 }'`
echo "Container ID:"$CONTAINER_ID
SHA_ID2=`docker inspect $CONTAINER_ID| jq .[0].Id|sed s/\"//g`
echo "SHA ID:"$SHA_ID2

if [ "$SHA_ID" != "$SHA_ID2" ]; then
  date=`date`
  echo "New image detected, restarting..."$date >>/tmp/check.out
  make stop
  make up
fi
