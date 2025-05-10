# Update version ONLY here
VERSION := 0.11.6
SHELL := /bin/bash
# Makefile for project
VENV := ~/.virtualenvs/fake.py/bin/activate
UNAME_S := $(shell uname -s)

# Build documentation using Sphinx and zip it
build_docs:
	source $(VENV) && sphinx-build -n -b text docs builddocs
	source $(VENV) && sphinx-build -n -a -b html docs builddocs
	cd builddocs && zip -r ../builddocs.zip . -x ".*" && cd ..

rebuild_docs:
	source $(VENV) && sphinx-apidoc . --full -o docs -H 'fake.py' -A 'Artur Barseghyan <artur.barseghyan@gmail.com>' -f -d 20
	cp docs/conf.py.distrib docs/conf.py
	cp docs/index.rst.distrib docs/index.rst

build_docs_epub:
	$(MAKE) -C docs/ epub

build_docs_pdf:
	$(MAKE) -C docs/ latexpdf

auto_build_docs:
	source $(VENV) && sphinx-autobuild docs docs/_build/html

pre-commit:
	pre-commit run --all-files

doc8:
	source $(VENV) && doc8

# Run ruff on the codebase
ruff:
	source $(VENV) && ruff check .

# Serve the built docs on port 5001
serve_docs:
	source $(VENV) && cd builddocs && python -m http.server 5001

# Install the project
install:
	source $(VENV) && pip install -e .[all]

test: clean
	source $(VENV) && pytest -vrx -s

test-integration: customisation-test \
dataclasses-test \
django-test \
hypothesis-test \
lazyfuzzy-test \
pydantic-test \
sqlalchemy-test \
sqlmodel-test \
tortoise-test


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
	source $(VENV) && cd examples/customisation/ && pytest

dataclasses-test:
	source $(VENV) && cd examples/dataclasses/ && pytest

django-test:
	source $(VENV) && cd examples/django/ && pytest

hypothesis-test:
	source $(VENV) && cd examples/hypothesis/ && pytest

lazyfuzzy-test:
	source $(VENV) && cd examples/lazyfuzzy/ && pytest

pydantic-test:
	source $(VENV) && cd examples/pydantic/ && pytest

sqlalchemy-test:
	source $(VENV) && cd examples/sqlalchemy/ && pytest

sqlmodel-test:
	source $(VENV) && cd examples/sqlmodel/ && pytest

tortoise-test:
	source $(VENV) && cd examples/tortoise/ && pytest

shell:
	source $(VENV) && ipython

customisation-shell:
	source $(VENV) && cd examples/customisation/ && python manage.py shell

customisation-address-cli:
	@echo Running Python script: $(filter-out $@,$(MAKECMDGOALS))
	source $(VENV) && cd examples/customisation/ && python address_cli.py $(filter-out $@,$(MAKECMDGOALS))

customisation-band-cli:
	@echo Running Python script: $(filter-out $@,$(MAKECMDGOALS))
	source $(VENV) && cd examples/customisation/ && python band_cli.py $(filter-out $@,$(MAKECMDGOALS))

customisation-custom-data-cli:
	@echo Running Python script: $(filter-out $@,$(MAKECMDGOALS))
	source $(VENV) && cd examples/customisation/ && python custom_data_cli.py $(filter-out $@,$(MAKECMDGOALS))

dataclasses-shell:
	source $(VENV) && cd examples/dataclasses/ && python manage.py shell

django-shell:
	source $(VENV) && python examples/django/manage.py shell

django-runserver:
	source $(VENV) && python examples/django/manage.py runserver 0.0.0.0:8000 --traceback -v 3

django-makemigrations:
	source $(VENV) && python examples/django/manage.py makemigrations

django-apply-migrations:
	source $(VENV) && python examples/django/manage.py migrate

lazyfuzzy-shell:
	source $(VENV) && cd examples/lazyfuzzy/ && python manage.py shell

pydantic-shell:
	source $(VENV) && cd examples/pydantic/ && python manage.py shell

sqlalchemy-shell:
	source $(VENV) && cd examples/sqlalchemy/ && python manage.py shell

sqlmodel-shell:
	source $(VENV) && cd examples/sqlmodel/ && python manage.py shell

tortoise-shell:
	source $(VENV) && cd examples/tortoise/ && python manage.py shell

create-secrets:
	source $(VENV) && detect-secrets scan > .secrets.baseline

detect-secrets:
	source $(VENV) && detect-secrets scan --baseline .secrets.baseline

# Clean up generated files
clean:
	find . -type f -name "*.pyc" -exec rm -f {} \;
	find . -type f -name "builddocs.zip" -exec rm -f {} \;
	find . -type f -name "*.py,cover" -exec rm -f {} \;
	find . -type f -name "*.orig" -exec rm -f {} \;
	find . -type f -name "*.coverage" -exec rm -f {} \;
	find . -type f -name "*.db" -exec rm -f {} \;
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
	rm -rf dist/
	rm -rf fake.py.egg-info/

compile-requirements:
	source $(VENV) && uv pip compile --all-extras -o docs/requirements.txt pyproject.toml

compile-requirements-upgrade:
	source $(VENV) && uv pip compile --all-extras -o docs/requirements.txt pyproject.toml --upgrade

update-version:
	#sed -i 's/version = "[0-9.]\+"/version = "$(VERSION)"/' pyproject.toml
	#sed -i 's/__version__ = "[0-9.]\+"/__version__ = "$(VERSION)"/' fake.py
	@echo "Updating version in pyproject.toml and fake.py"
	@if [ "$(UNAME_S)" = "Darwin" ]; then \
		gsed -i 's/version = "[0-9.]\+"/version = "$(VERSION)"/' pyproject.toml; \
		gsed -i 's/__version__ = "[0-9.]\+"/__version__ = "$(VERSION)"/' fake.py; \
	else \
		sed -i 's/version = "[0-9.]\+"/version = "$(VERSION)"/' pyproject.toml; \
		sed -i 's/__version__ = "[0-9.]\+"/__version__ = "$(VERSION)"/' fake.py; \
	fi

build:
	source $(VENV) && python -m build .

check-build:
	source $(VENV) && twine check dist/*

release:
	source $(VENV) && twine upload dist/* --verbose

test-release:
	source $(VENV) && twine upload --repository testpypi dist/*

mypy:
	source $(VENV) && mypy fake.py

%:
	@:
