# Update version ONLY here
VERSION := 0.12.2
SHELL := /bin/bash
# Makefile for project
VENV := .venv/bin/activate
UNAME_S := $(shell uname -s)

# Build documentation using Sphinx and zip it
build-docs:
	uv run sphinx-source-tree
	uv run sphinx-build -n -a -b markdown docs builddocs
	uv run sphinx-build -n -a -b html docs builddocs
	cd builddocs && zip -r ../builddocs.zip . -x ".*" && cd ..

rebuild-docs:
	uv run sphinx-apidoc . --full -o docs -H 'fake.py' -A 'Artur Barseghyan <artur.barseghyan@gmail.com>' -f -d 20
	cp docs/conf.py.distrib docs/conf.py
	cp docs/index.rst.distrib docs/index.rst

build-docs-epub:
	$(MAKE) -C docs/ epub

build-docs-pdf:
	$(MAKE) -C docs/ latexpdf

build-docs-markdown:
	$(MAKE) -C docs/ markdown

auto-build-docs:
	uv run sphinx-autobuild docs docs/_build/html --port 5001

# Serve the built docs on port 5001
serve-docs:
	uv run python -m http.server 5001 --directory builddocs/

pre-commit:
	uv run pre-commit run --all-files

doc8:
	uv run doc8

# Run ruff on the codebase
ruff:
	uv run ruff check . --fix
	uv run ruff format .

create-venv:
	uv venv

# Install the project
install:
	uv sync --all-extras

test: clean
	uv run pytest -vrx -s

test-integration: customisation-test \
dataclasses-test \
django-test \
hypothesis-test \
lazyfuzzy-test \
pydantic-test \
sqlalchemy-test \
sqlmodel-test \
tortoise-test

install-django:
	uv pip install -r examples/django/requirements.in

install-hypothesis:
	uv pip install -r examples/hypothesis/requirements.in

install-pydantic:
	uv pip install -r examples/pydantic/requirements.in

install-sqlalchemy:
	uv pip install -r examples/sqlalchemy/requirements.in

install-sqlmodel:
	uv pip install -r examples/sqlmodel/requirements.in

install-tortoise:
	uv pip install -r examples/tortoise/requirements.in

install-all: install \
install-django \
install-hypothesis \
install-pydantic \
install-sqlalchemy \
install-sqlmodel \
install-tortoise

test-all: test \
customisation-test \
dataclasses-test \
django-test \
hypothesis-test \
lazyfuzzy-test \
pydantic-test \
sqlalchemy-test \
sqlmodel-test \
tortoise-test

customisation-test:
	cd examples/customisation/ && uv run pytest

dataclasses-test:
	cd examples/dataclasses/ && uv run pytest

django-test:
	cd examples/django/ && uv run pytest

hypothesis-test:
	cd examples/hypothesis/ && uv run pytest

lazyfuzzy-test:
	cd examples/lazyfuzzy/ && uv run pytest

pydantic-test:
	cd examples/pydantic/ && uv run pytest

sqlalchemy-test:
	cd examples/sqlalchemy/ && uv run pytest

sqlmodel-test:
	cd examples/sqlmodel/ && uv run pytest

tortoise-test:
	cd examples/tortoise/ && uv run pytest

shell:
	uv run ipython

customisation-shell:
	cd examples/customisation/ && uv run python manage.py shell

customisation-address-cli:
	@echo Running Python script: $(filter-out $@,$(MAKECMDGOALS))
	cd examples/customisation/ && uv run python address_cli.py $(filter-out $@,$(MAKECMDGOALS))

customisation-band-cli:
	@echo Running Python script: $(filter-out $@,$(MAKECMDGOALS))
	cd examples/customisation/ && uv run python band_cli.py $(filter-out $@,$(MAKECMDGOALS))

customisation-custom-data-cli:
	@echo Running Python script: $(filter-out $@,$(MAKECMDGOALS))
	cd examples/customisation/ && uv run python custom_data_cli.py $(filter-out $@,$(MAKECMDGOALS))

dataclasses-shell:
	cd examples/dataclasses/ && uv run python manage.py shell

django-shell:
	cd examples/django/ && uv run python manage.py shell

django-runserver:
	cd examples/django/ && uv run python manage.py runserver 0.0.0.0:8000 --traceback -v 3

django-makemigrations:
	cd examples/django/ && uv run python manage.py makemigrations

django-apply-migrations:
	cd examples/django/ && uv run python manage.py migrate

lazyfuzzy-shell:
	cd examples/lazyfuzzy/ && uv run python manage.py shell

pydantic-shell:
	cd examples/pydantic/ && uv run python manage.py shell

sqlalchemy-shell:
	cd examples/sqlalchemy/ && uv run python manage.py shell

sqlmodel-shell:
	cd examples/sqlmodel/ && uv run python manage.py shell

tortoise-shell:
	cd examples/tortoise/ && uv run python manage.py shell

create-secrets:
	uv run detect-secrets scan > .secrets.baseline

detect-secrets:
	uv run detect-secrets scan --baseline .secrets.baseline

# Clean up generated files
clean:
	find . -type f -name "*.pyc" -exec rm -f {} \;
	find . -type f -name "builddocs.zip" -exec rm -f {} \;
	find . -type f -name "*.py,cover" -exec rm -f {} \;
	find . -type f -name "*.orig" -exec rm -f {} \;
	find . -type d -name "__pycache__" -exec rm -rf {} \; -prune
	rm -rf build/
	rm -rf dist/
	rm -rf .cache/
	rm -rf htmlcov/
	rm -rf builddocs/
	rm -rf testdocs/
	rm -rf .coverage
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	rm -rf fake.py.egg-info/

compile-requirements:
	uv pip compile --all-extras -o docs/requirements.txt pyproject.toml

compile-requirements-upgrade:
	uv pip compile --all-extras -o docs/requirements.txt pyproject.toml --upgrade

update-version:
	@echo "Updating version in pyproject.toml and fake.py"
	@if [ "$(UNAME_S)" = "Darwin" ]; then \
		gsed -i 's/version = "[0-9.]\+"/version = "$(VERSION)"/' pyproject.toml; \
		gsed -i 's/__version__ = "[0-9.]\+"/__version__ = "$(VERSION)"/' fake.py; \
	else \
		sed -i 's/version = "[0-9.]\+"/version = "$(VERSION)"/' pyproject.toml; \
		sed -i 's/__version__ = "[0-9.]\+"/__version__ = "$(VERSION)"/' fake.py; \
	fi

build:
	uv run python -m build .

check-build:
	uv run twine check dist/*

release:
	uv run twine upload dist/* --verbose

test-release:
	uv run twine upload --repository testpypi dist/*

mypy:
	uv run mypy fake.py

%:
	@:
