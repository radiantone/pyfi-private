/usr/bin/supervisord
echo "Sleeping 10 seconds..."
sleep 10
echo "Resuming..."
tail -f /opt/pyfi/*log
