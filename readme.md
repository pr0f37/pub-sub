# Running instructions
## RabbitMQ setup
```sh
docker network create rabbits
docker run -d --rm --net rabbits --hostname rabbit-1 --name rabbit-1 -p 5672:5672 -p 15672:15672 rabbitmq:3.11-management
docker exec -it rabbit-1 bash
```
## Publisher setup

```sh
cd applications/publisher
docker build -t prophet/publisher .
docker run -it --rm -e RABBIT_HOST=rabbit-1 -e RABBIT_PORT=5672 -e RABBIT_USERNAME=guest -e RABBIT_PASSWORD=guest -e RABBIT_QUEUE=task_queue --net rabbits --name flask-publisher -p 5000:5000 prophet/publisher 
```

## Consumer setup

```sh
cd applications/consumer 
docker build -t prophet/consumer .
docker run -it --rm -e RABBIT_HOST=rabbit-1 -e RABBIT_PORT=5672 -e RABBIT_USERNAME=guest -e RABBIT_PASSWORD=guest -e RABBIT_QUEUE=task_queue --net rabbits --name consumer prophet/consumer 
```