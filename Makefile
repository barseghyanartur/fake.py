# Update version ONLY here
VERSION := 0.3
SHELL := /bin/bash
# Makefile for project
VENV := ~/.virtualenvs/fake.py/bin/activate

# Build documentation using Sphinx and zip it
build_docs:
	source $(VENV) && sphinx-build -n -a -b html docs builddocs
	cd builddocs && zip -r ../builddocs.zip . -x ".*" && cd ..

rebuild_docs:
	source $(VENV) && sphinx-apidoc . --full -o docs -H 'fake.py' -A 'Artur Barseghyan <artur.barseghyan@gmail.com>' -f -d 20
	#cp docs/conf.py.distrib docs/conf.py
	cp docs/index.rst.distrib docs/index.rst

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

# Serve the built docs on port 5000
serve_docs:
	source $(VENV) && cd builddocs && python -m http.server 5000

# Install the project
install:
	source $(VENV) && pip install -e .[all]

test:
	source $(VENV) && pytest -vrx -s

shell:
	source $(VENV) && ipython

django-shell:
	source $(VENV) && python examples/django/manage.py shell

pydantic-shell:
	source $(VENV) && python examples/pydantic/shell.py

dataclasses-shell:
	source $(VENV) && python examples/dataclasses/shell.py

tortoise-shell:
	source $(VENV) && python examples/tortoise/shell.py

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

compile-requirements:
	source $(VENV) && python -m piptools compile --extra all -o docs/requirements.txt pyproject.toml

update-version:
	#sed -i 's/"version": "[0-9.]\+"/"version": "$(VERSION)"/' package.json
	sed -i 's/version = "[0-9.]\+"/version = "$(VERSION)"/' pyproject.toml
	sed -i 's/__version__ = "[0-9.]\+"/__version__ = "$(VERSION)"/' fake.py
#	find src/ -type f -name '*.css' -exec sed -i 's/@version [0-9.]\+/@version $(VERSION)/' {} \;
#	find src/ -type f -name '*.js' -exec sed -i 's/@version [0-9.]\+/@version $(VERSION)/' {} \;

build:
	source $(VENV) && python -m build .

check-build:
	source $(VENV) && twine check dist/*

release:
	source $(VENV) && twine upload dist/* --verbose

test-release:
	source $(VENV) && twine upload --repository testpypi dist/*

mypy:
	mypy .
