#/usr/bin/supervisord
echo "Sleeping 10 seconds..."
sleep 10
service supervisor stop
#venv/bin/pyfi --config --db postgresql://postgres:pyfi101@postgres:5432/pyfi --broker pyamqp://rabbitmq --backend redis://redis
echo "Resuming..."
touch /opt/pyfi/agent.log
supervisord -n -c supervisord.conf &
tail -f /opt/pyfi/*log
