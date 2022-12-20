### Defensive settings for make:
#     https://tech.davis-hansson.com/p/make/
SHELL:=bash
.ONESHELL:
.SHELLFLAGS:=-xeu -o pipefail -O inherit_errexit -c
.SILENT:
.DELETE_ON_ERROR:
MAKEFLAGS+=--warn-undefined-variables
MAKEFLAGS+=--no-builtin-rules

# We like colors
# From: https://coderwall.com/p/izxssa/colored-makefile-for-golang-projects
RED=`tput setaf 1`
GREEN=`tput setaf 2`
RESET=`tput sgr0`
YELLOW=`tput setaf 3`

PLONE_VERSION=6.0.0.1

ifndef LOG_LEVEL
	LOG_LEVEL=INFO
endif

CURRENT_USER=$$(whoami)
USER_INFO=$$(id -u ${CURRENT_USER}):$$(getent group ${CURRENT_USER}|cut -d: -f3)

BACKEND_FOLDER=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

CODE_QUALITY_VERSION=2.0.2
LINT=docker run -e LOG_LEVEL="${LOG_LEVEL}" --rm -v "${BACKEND_FOLDER}":/github/workspace plone/code-quality:${CODE_QUALITY_VERSION} check
FORMAT=docker run --user="${USER_INFO}" -e LOG_LEVEL="${LOG_LEVEL}" --rm -v "${BACKEND_FOLDER}":/github/workspace plone/code-quality:${CODE_QUALITY_VERSION} format

PACKAGE_NAME=ploneorgbr.core
PACKAGE_PATH=src/ploneorgbr.core/src/
IMAGE_NAME=ploneorgbr/site-backend
IMAGE_TAG=latest
CHECK_PATH=src/ploneorgbr.core/setup.py scripts/ $(PACKAGE_PATH)

# Add the following 'help' target to your Makefile
# And add help text after each target name starting with '\#\#'
.PHONY: help
help: ## This help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: clean
clean: clean-build clean-pyc clean-test clean-venv clean-instance ## remove all build, test, coverage and Python artifacts

.PHONY: clean-instance
clean-instance: ## remove existing instance
	rm -fr instance etc inituser var

.PHONY: clean-venv
clean-venv: ## remove virtual environment
	rm -fr bin include lib lib64

.PHONY: clean-build
clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -rf {} +

.PHONY: clean-pyc
clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

.PHONY: clean-test
clean-test: ## remove test and coverage artifacts
	rm -f .coverage
	rm -fr htmlcov/

bin/pip:
	@echo "$(GREEN)==> Setup Virtual Env$(RESET)"
	python3 -m venv .
	bin/pip install -U "pip" "wheel" "cookiecutter"

instance/etc/zope.ini:	bin/pip
	@echo "$(GREEN)==> Install Plone and create instance$(RESET)"
	bin/pip install Plone -c https://dist.plone.org/release/$(PLONE_VERSION)/constraints.txt
	bin/cookiecutter -f --no-input --config-file instance.yaml https://github.com/plone/cookiecutter-zope-instance
	mkdir -p var/{filestorage,blobstorage,cache,log}

# i18n
bin/i18ndude:	bin/pip
	@echo "$(GREEN)==> Install translation tools$(RESET)"
	bin/pip install i18ndude

.PHONY: i18n
i18n: bin/i18ndude ## Update locales
	@echo "$(GREEN)==> Updating locales$(RESET)"
	bin/update_locale

.PHONY: build
build: instance/etc/zope.ini ## Create virtualenv and run buildout
	@echo "$(GREEN)==> Setup Build$(RESET)"
	bin/pip install -r requirements.txt

.PHONY: build
build-dev: instance/etc/zope.ini ## Create virtualenv and run buildout
	@echo "$(GREEN)==> Setup Build$(RESET)"
	bin/pip install -r requirements/dev.txt

.PHONY: format
format: ## Format the codebase according to our standards
	@echo "$(GREEN)==> Format codebase$(RESET)"
	$(FORMAT)

.PHONY: format-black
format-black:  ## Format the codebase with black
	@echo "$(GREEN)==> Format codebase with black$(RESET)"
	$(FORMAT) black ${CODEPATH}

.PHONY: format-isort
format-isort:  ## Format the codebase with isort
	@echo "$(GREEN)==> Format codebase with isort$(RESET)"
	$(FORMAT) isort ${CODEPATH}

.PHONY: format-zpretty
format-zpretty:  ## Format the codebase with zpretty
	@echo "$(GREEN)==> Format codebase with zpretty$(RESET)"
	$(FORMAT) zpretty ${CODEPATH}

.PHONY: lint
lint:## check code style
	$(LINT)

.PHONY: lint-black
lint-black: ## validate black formating
	$(LINT) black ${CODEPATH}

.PHONY: lint-flake8
lint-flake8: ## validate black formating
	$(LINT) flake8 ${CODEPATH}

.PHONY: lint-isort
lint-isort: ## validate using isort
	$(LINT) isort ${CODEPATH}

.PHONY: lint-zpretty
lint-zpretty: ## validate ZCML/XML using zpretty
	$(LINT) zpretty ${CODEPATH}

.PHONY: test
test: ## run tests
	./bin/zope-testrunner --auto-color --auto-progress --test-path src/ploneorgbr.core/src/

.PHONY: test_quiet
test_quiet: ## run tests removing deprecation warnings
	PYTHONWARNINGS=ignore ./bin/zope-testrunner --auto-color --auto-progress --test-path src/ploneorgbr.core/src/

.PHONY: create-site
create-site: instance/etc/zope.ini ## Create a new site from scratch
	PYTHONWARNINGS=ignore ./bin/zconsole run instance/etc/zope.conf ./scripts/create_site.py

.PHONY: console
console: instance/etc/zope.ini ## Open a console
	PYTHONWARNINGS=ignore ./bin/zconsole debug instance/etc/zope.conf

.PHONY: start
start: ## Start a Plone instance on localhost:8080
	PYTHONWARNINGS=ignore ./bin/runwsgi instance/etc/zope.ini

.PHONY: build-image
build-image:  ## Build Docker Image
	@docker build . -t $(IMAGE_NAME):$(IMAGE_TAG) -f Dockerfile --build-arg PLONE_VERSION=$(PLONE_VERSION)
