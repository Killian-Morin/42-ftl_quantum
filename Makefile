NAME = ftl_quantum

all : down build run connect

run:
	docker-compose -p ${NAME} up -d

build:
	docker-compose -p ${NAME} build

connect:
	docker exec -it ftl_quantum /bin/bash

down:
	docker-compose -p ${NAME} down

clean: down
	docker system prune -af

.PHONY: all run down clean connect