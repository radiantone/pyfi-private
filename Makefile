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
	pytest

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
refresh:
	./bin/docker-refresh.sh

.PHONY: update
update: freeze format lint
	git add setup.py docs bin pyfi ui *.txt Makefile
	git commit --allow-empty -m "Updates"
	git push origin main
	python setup.py install
	git status

.PHONY: docs
docs:
	cd docs
	make -C docs html

.PHONY: release
release: update tests docs 
	bash ./bin/tag.sh

.PHONY: freeze
freeze:
	pip freeze |grep -v pyfi > requirements-dev.txt

.PHONY: clean
clean:
	python setup.py clean
	git status

.PHONY: all
all: format lint freeze update docs install clean
	git status
