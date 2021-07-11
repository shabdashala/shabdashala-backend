export LC_CTYPE="en_US.UTF-8"

.DEFAULT_GOAL := help
.PHONY: docs migrate

create-postgres-extensions:
	psql -U root -d template1 -c 'create extension citext;'
	psql -U root -d template1 -c 'create extension hstore;'
	psql -U root -d template1 -c 'create extension cube;'
	psql -U root -d template1 -c 'create extension earthdistance;'

recreate-db:
	psql -U root -d postgres -c 'drop database shabdashala_devdb;'
	psql -U root -d postgres -c 'create database shabdashala_devdb;'
	make migrate

migrate:
	python manage.py migrate --noinput

deps:
	pip install -r requirements.txt
	make migrate

nb:
	python manage.py shell_ipynb

shell:
	python manage.py shell_plus

pre:
	git add -u && pre-commit
	@echo "If there are new files, 'git add' them and run 'make pre' again."

docs:
	cd docs && make html

help: ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'
