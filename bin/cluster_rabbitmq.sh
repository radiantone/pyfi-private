docker exec -it rabbitmq2 bash -c  "rabbitmqctl stop_app"
docker exec -it rabbitmq2 bash -c  "rabbitmqctl join_cluster rabbit@rabbitmq"
docker exec -it rabbitmq2 bash -c  "rabbitmqctl start_app"
