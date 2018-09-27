help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo "  build         builds docker-compose containers"
	@echo "  up            starts docker-compose containers"
	@echo "  down          stops the running docker-compose containers"
	@echo "  rebuild       rebuilds the image from scratch without using any cached layers"
	@echo "  test          starts run unittest inside web container."
	@echo "  lint          use pylint to check all .py files"


build:
	sudo docker-compose -f local.yaml build

up:
	sudo docker-compose -f local.yaml up

down:
	sudo docker-compose -f local.yaml stop

rebuild:
	sudo docker-compose -f local.yaml build --no-cache

test:
	sudo docker-compose -f local.yaml exec tornado python run_test.py

lint:
	sudo docker-compose -f local.yaml exec tornado pylint --rcfile 3rds/pylint/pylint.txt -f colorized --ignore-patterns test*.py *.py
