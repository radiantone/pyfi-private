.DEFAULT_GOAL := all
black = black --target-version py39 pyfi
isort = isort --profile black pyfi
flake8 = flake8 --ignore=E203,F401,E402,F841,E501,E722,W503 pyfi

.PHONY: depends
depends:
	echo

.PHONY: init
init: depends
	echo "Setting up virtual environment in venv/"
	python3 -m venv venv
	echo "Virtual environment complete."

.PHONY: test
test:
	pytest pyfi/tests

.PHONY: format
format:
	$(isort)
	$(black)

.PHONY: lint
lint:
	mypy --show-error-codes pyfi
	$(flake8)
	$(isort) --check-only --df
	$(black) --check --diff

.PHONY: install
install: depends init
	pip install -r requirements.txt
	python setup.py install
	python setup.py clean

.PHONY: up
up:
	./bin/up.sh

.PHONY: stop
stop:
	docker compose stop

.PHONY: refresh
refresh: stop
	./bin/docker-refresh.sh

.PHONY: update
update: freeze format lint
	git add diary.md setup.py docs bin pyfi ui *.txt Makefile
	git add docker-*
	git add docker/
	git commit --allow-empty -m "Updates"
	git push origin develop
	python setup.py install
	git status

.PHONY: ui
ui:
	cd ui; quasar build

.PHONY: docs
docs:
	make -C docs html

.PHONY: release
release: update tests docs 
	bash ./bin/tag.sh

.PHONY: freeze
freeze:
	pip freeze |grep -v pyfi > requirements-dev.txt
	pip freeze |grep -v pyfi > requirements.txt

.PHONY: clean
clean:
	python setup.py clean
	-find . -type d -name __pycache__ -print -exec rm -rf {} \; 2> /dev/null
	git status

.PHONY: build
build:
	docker compose build nginx api

.PHONY: push
push:
	aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 013035288901.dkr.ecr.us-east-1.amazonaws.com
	docker tag pyfi/api:latest 013035288901.dkr.ecr.us-east-1.amazonaws.com/api:latest
	docker push  013035288901.dkr.ecr.us-east-1.amazonaws.com/api:latest

	docker tag nginx:latest 013035288901.dkr.ecr.us-east-1.amazonaws.com/nginx:latest
	docker push  013035288901.dkr.ecr.us-east-1.amazonaws.com/nginx:latest

	docker tag rabbitmq:management 013035288901.dkr.ecr.us-east-1.amazonaws.com/rabbitmq:management
	docker push  013035288901.dkr.ecr.us-east-1.amazonaws.com/rabbitmq:management

	docker tag rabbitmq:management 013035288901.dkr.ecr.us-east-1.amazonaws.com/rabbitmq:management
	docker push  013035288901.dkr.ecr.us-east-1.amazonaws.com/rabbitmq:management

	docker tag postgres:latest 013035288901.dkr.ecr.us-east-1.amazonaws.com/postgres:latest
	docker push  013035288901.dkr.ecr.us-east-1.amazonaws.com/postgres:latest

	docker tag pyfi/clientsocket:latest 013035288901.dkr.ecr.us-east-1.amazonaws.com/clientsocket:latest
	docker push  013035288901.dkr.ecr.us-east-1.amazonaws.com/clientsocket:latest


.PHONY: all
all: format lint freeze update docs install clean
	git status
