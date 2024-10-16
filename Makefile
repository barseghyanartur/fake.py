# Update version ONLY here
VERSION := 0.11.2
SHELL := /bin/bash
# Makefile for project
VENV := ~/.virtualenvs/fake.py/bin/activate

# Build documentation using Sphinx and zip it
build_docs:
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

pre-commit:
	pre-commit run --all-files

# Format code using Black
black:
	source $(VENV) && black .

# Sort imports using isort
isort:
	source $(VENV) && isort . --overwrite-in-place

doc8:
	source $(VENV) && doc8

# Run ruff on the codebase
ruff:
	source $(VENV) && ruff .

# Serve the built docs on port 5001
serve_docs:
	source $(VENV) && cd builddocs && python -m http.server 5001

# Install the project
install:
	source $(VENV) && pip install -e .[all]

test: clean
	source $(VENV) && pytest -vrx -s

test-all: test \
customization-test \
dataclasses-test \
django-test \
hypothesis-test \
lazyfuzzy-test \
pydantic-test \
sqlalchemy-test \
sqlmodel-test \
tortoise-test

customization-test:
	source $(VENV) && cd examples/customization/ && python manage.py test

dataclasses-test:
	source $(VENV) && cd examples/dataclasses/ && python manage.py test

django-test:
	source $(VENV) && cd examples/django/ && ./manage.py test

hypothesis-test:
	source $(VENV) && cd examples/hypothesis/ && python manage.py test

lazyfuzzy-test:
	source $(VENV) && cd examples/lazyfuzzy/ && python manage.py test

pydantic-test:
	source $(VENV) && cd examples/pydantic/ && python manage.py test

sqlalchemy-test:
	source $(VENV) && cd examples/sqlalchemy/ && python manage.py test

sqlmodel-test:
	source $(VENV) && cd examples/sqlmodel/ && python manage.py test

tortoise-test:
	source $(VENV) && cd examples/tortoise/ && python manage.py test

shell:
	source $(VENV) && ipython

customization-shell:
	source $(VENV) && cd examples/customization/ && python manage.py shell

customization-address-cli:
	@echo Running Python script: $(filter-out $@,$(MAKECMDGOALS))
	source $(VENV) && cd examples/customization/ && python address_cli.py $(filter-out $@,$(MAKECMDGOALS))

customization-band-cli:
	@echo Running Python script: $(filter-out $@,$(MAKECMDGOALS))
	source $(VENV) && cd examples/customization/ && python band_cli.py $(filter-out $@,$(MAKECMDGOALS))

customization-custom-data-cli:
	@echo Running Python script: $(filter-out $@,$(MAKECMDGOALS))
	source $(VENV) && cd examples/customization/ && python custom_data_cli.py $(filter-out $@,$(MAKECMDGOALS))

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

compile-requirements-pip-tools:
	source $(VENV) && python -m piptools compile --all-extras -o docs/requirements.txt pyproject.toml

compile-requirements-upgrade-pip-tools:
	source $(VENV) && python -m piptools compile --all-extras -o docs/requirements.txt pyproject.toml --upgrade

compile-requirements:
	source $(VENV) && uv pip compile --all-extras -o docs/requirements.txt pyproject.toml

compile-requirements-upgrade:
	source $(VENV) && uv pip compile --all-extras -o docs/requirements.txt pyproject.toml --upgrade

update-version:
	#sed -i 's/"version": "[0-9.]\+"/"version": "$(VERSION)"/' package.json
	sed -i 's/version = "[0-9.]\+"/version = "$(VERSION)"/' pyproject.toml
	sed -i 's/__version__ = "[0-9.]\+"/__version__ = "$(VERSION)"/' fake.py
#	find src/ -type f -name '*.css' -exec sed -i 's/@version [0-9.]\+/@version $(VERSION)/' {} \;
#	find src/ -type f -name '*.js' -exec sed -i 's/@version [0-9.]\+/@version $(VERSION)/' {} \;

update-security:
	@echo "Updating SECURITY.rst with VERSION=$(VERSION)"
	# Extract major and minor version (e.g., 0.10 from 0.10.2) \
	MAJOR_MINOR=$(echo $(VERSION) | cut -d. -f1,2);
	# Extract major and minor numbers \
	MAJOR=$(echo $$MAJOR_MINOR | cut -d. -f1);
	MINOR=$(echo $$MAJOR_MINOR | cut -d. -f2);
	# Calculate previous minor version (e.g., 0.9 from 0.10) \
	PREV_MINOR=$$(expr $$MINOR - 1);
	PREV_MAJOR_MINOR=$$MAJOR.$$PREV_MINOR;
	# Define fixed column widths \
	VERSION_COL_WIDTH=15;
	SUPPORTED_COL_WIDTH=16;
	# Function to pad strings to fixed width \
	pad() { printf "%%-%ds" "$$VERSION_COL_WIDTH" "$$1"; }; \
	# Pad version strings \
	VER1=`pad "$(MAJOR_MINOR).x"`; \
	VER2=`pad "$$PREV_MAJOR_MINOR.x"`; \
	VER3=`pad "< $$PREV_MAJOR_MINOR"`; \
	# Generate the new Supported Versions table \
	NEW_TABLE=".. code-block:: text\n\n\
    ┌─────────────────┬────────────────┐\n\
    │ Version         │ Supported      │\n\
    ├─────────────────┼────────────────┤\n\
    │ $$VER1 │ Yes            │\n\
    ├─────────────────┼────────────────┤\n\
    │ $$VER2 │ Yes            │\n\
    ├─────────────────┼────────────────┤\n\
    │ $$VER3 │ No             │\n\
    └─────────────────┴────────────────┘"; \
	\
	# Replace the existing Supported Versions table in SECURITY.rst \
	echo $(NEW_TABLE); \
	sed -i '' '/^.. code-block:: text$/,/^$/c\'"$$NEW_TABLE" SECURITY.rst

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
