.DEFAULT_GOAL := all
black = black --target-version py39 pyfi
isort = isort --profile black pyfi
flake8 = flake8 --ignore=E203,F401,E402,F841,E501,E722,W503 pyfi
nvm = . ${NVM_DIR}/nvm.sh
NODE_OPTIONS=--openssl-legacy-provider

.PHONY: depends
depends:
	./bin/depends.sh

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
	eslint --ext .js,.ts --fix ui/src/components #.vue

.PHONY: lint
lint:
	mypy --show-error-codes pyfi
	$(flake8)
	$(isort) --check-only --df
	$(black) --check --diff
	eslint --ext .js,.ts  ui/src/components #,.vue

.PHONY: install
install: depends init
	pip install -r requirements.txt
	python setup.py install
	python setup.py clean

.PHONY: deploy
deploy: login pull up

.PHONY: pull
pull: login
	docker compose pull nginx api clientsocket rabbitmq

.PHONY: up
up:
	docker compose up -d mindsdb postgresdb redis rabbitmq rabbitmq2 websockets websockets2 nginx globalsocket clientsocket mongodb web pgadmin api influxdb mindsdb

.PHONY: stop
stop:
	@docker compose stop

.PHONY: refresh
refresh: stop
	@./bin/docker-refresh.sh

.PHONY: update
update: freeze format lint
	git add diary.md setup.py docs bin pyfi ui *.txt Makefile
	git add docker-*
	git add docker/
	git commit --allow-empty -m "Updates"
	git push origin production
	python setup.py install
	git status

.PHONY: install-ui
install-ui:
	cd ui; npm install

.PHONY: ui
ui:
	( cd ui; SOCKETIO=https://app.elasticcode.ai quasar build; /usr/bin/git add -f dist/spa )

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
	-find . -type d -name __pycache__ -exec rm -rf {} \; 2> /dev/null
	git status
	exit 0

.PHONY: build-clean
build-clean:
	make ui ; \
	docker buildx bake  --no-cache ;\


.PHONY: build
build: format
	@read -p "Build UI? [y/N] " ans && ans=$${ans:-N} ; \
    if [ $${ans} = y ] || [ $${ans} = Y ]; then \
        make ui ; \
		docker buildx bake ;\
		docker tag pyfi/processor:latest pyfi/processor:production ;\
    else \
		docker buildx bake ;\
		docker tag pyfi/processor:latest pyfi/processor:production ;\
    fi

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

	docker tag postgres:14 013035288901.dkr.ecr.us-east-1.amazonaws.com/postgres:production
	docker push  013035288901.dkr.ecr.us-east-1.amazonaws.com/postgres:production

	docker tag postgres:14 013035288901.dkr.ecr.us-east-1.amazonaws.com/web:production
	docker push  013035288901.dkr.ecr.us-east-1.amazonaws.com/web:production

	docker push  013035288901.dkr.ecr.us-east-1.amazonaws.com/clientsocket:production

	docker push  013035288901.dkr.ecr.us-east-1.amazonaws.com/globalsocket:production

	# Remove local remote tags
	docker rmi 013035288901.dkr.ecr.us-east-1.amazonaws.com/globalsocket:production
	docker rmi 013035288901.dkr.ecr.us-east-1.amazonaws.com/clientsocket:production
	docker rmi 013035288901.dkr.ecr.us-east-1.amazonaws.com/postgres:production
	docker rmi 013035288901.dkr.ecr.us-east-1.amazonaws.com/rabbitmq:production
	docker rmi 013035288901.dkr.ecr.us-east-1.amazonaws.com/nginx:production

.PHONY: all
all: format lint freeze update docs install clean
	git status
