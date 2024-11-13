NAME = ftl_quantum

all : build run connect

run:
	docker-compose -p ${NAME} up -d

check_env:
	@if [ ! -f .env ]; then \
		echo ".env file is missing. Please add it before running this target."; \
		exit 1; \
	fi

build: check_env
	docker-compose -p ${NAME} build

connect:
	docker exec -it ${NAME} /bin/bash

down:
	docker-compose -p ${NAME} down

clean: down
	docker system prune -af

fclean: clean
	rm -f exercices/*.png
	rm -f exercices/ex*/*.png

.PHONY: all run check_env build connect down clean fclean