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

.PHONY: deploy
deploy: login pull up

.PHONY: pull
pull:
	docker compose pull nginx api clientsocket rabbitmq

.PHONY: up
up:
	docker compose up -d postgresdb redis rabbitmq rabbitmq2 websockets websockets2 nginx globalsocket clientsocket mongodb web api

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

.PHONY: install-ui
install-ui:
	cd ui; npm install

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
	./bin/docker-refresh.sh
	python setup.py clean
	-find . -type d -name __pycache__ -print -exec rm -rf {} \; 2> /dev/null
	git status

.PHONY: build
build:
	docker compose build

.PHONY: login
login:
	. venv/bin/activate && ( \
		aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 013035288901.dkr.ecr.us-east-1.amazonaws.com \
	)

.PHONY: push
push:
	aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 013035288901.dkr.ecr.us-east-1.amazonaws.com

	docker tag rabbitmq:management 013035288901.dkr.ecr.us-east-1.amazonaws.com/rabbitmq:production
	docker push  013035288901.dkr.ecr.us-east-1.amazonaws.com/rabbitmq:production

	docker tag rabbitmq:management 013035288901.dkr.ecr.us-east-1.amazonaws.com/rabbitmq:production
	docker push  013035288901.dkr.ecr.us-east-1.amazonaws.com/rabbitmq:production

	docker tag postgres:latest 013035288901.dkr.ecr.us-east-1.amazonaws.com/postgres:production
	docker push  013035288901.dkr.ecr.us-east-1.amazonaws.com/postgres:production

	docker tag pyfi/clientsocket:latest 013035288901.dkr.ecr.us-east-1.amazonaws.com/clientsocket:production
	docker push  013035288901.dkr.ecr.us-east-1.amazonaws.com/clientsocket:production

	docker tag pyfi/websockets:latest 013035288901.dkr.ecr.us-east-1.amazonaws.com/globalsocket:production
	docker push  013035288901.dkr.ecr.us-east-1.amazonaws.com/globalsocket:production

.PHONY: all
all: format lint freeze update docs install clean
	git status
