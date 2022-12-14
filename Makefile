.PHONY: console migrate migrations server dependencies

# DEVELOPMENT
# ~~~~~~~~~~~
# The following rules can be used during development in order to launch development server, generate
# locales, etc.
# --------------------------------------------------------------------------------------------------

shell:
	python manage.py shell_plus

migrate:
	python manage.py migrate

migrations:
	python manage.py makemigrations

server:
	python manage.py runserver

dependencies:
	poetry lock; poetry run poe export; poetry run poe export_dev

# QUALITY ASSURANCE
# ~~~~~~~~~~~~~~~~~
# The following rules can be used to check code quality, import sorting, etc.
# --------------------------------------------------------------------------------------------------

.PHONY: quality fix pylint
quality:
	black --check lacommunaute
	isort --check --profile black lacommunaute
	flake8 lacommunaute --count --show-source --statistics

fix:
	black lacommunaute
	isort --profile black lacommunaute
	flake8 lacommunaute
	djhtml --in-place $(shell find lacommunaute/templates -name "*.html")

pylint:
	pylint lacommunaute


# Docker shell.
# =============================================================================

.PHONY: shell_on_postgres_container

shell_on_postgres_container:
	docker exec -ti postgres /bin/bash


# Postgres CLI.
# =============================================================================

.PHONY: psql

# Connect to the `postgres` container as the POSTGRES_USER user.
psql:
	docker exec -ti -e PGPASSWORD=$(POSTGRES_PASSWORD) commu_postgres psql -U $(POSTGRES_USER)
