docker run -d  -p 4369:4369 -p 5671:5671 -p 5672:5672 -p 15672:15672 rabbitmq
docker exec 2d857602b1f5 rabbitmq-plugins enable rabbitmq_management
