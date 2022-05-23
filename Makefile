### Defensive settings for make:
#     https://tech.davis-hansson.com/p/make/
SHELL:=bash
.ONESHELL:
.SHELLFLAGS:=-xeu -o pipefail -O inherit_errexit -c
.SILENT:
.DELETE_ON_ERROR:
MAKEFLAGS+=--warn-undefined-variables
MAKEFLAGS+=--no-builtin-rules

CURRENT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))


# We like colors
# From: https://coderwall.com/p/izxssa/colored-makefile-for-golang-projects
RED=`tput setaf 1`
GREEN=`tput setaf 2`
RESET=`tput sgr0`
YELLOW=`tput setaf 3`

.PHONY: all
all: build

# Add the following 'help' target to your Makefile
# And add help text after each target name starting with '\#\#'
.PHONY: help
help: ## This help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: install-frontend
install-frontend:  ## Install React Frontend
	$(MAKE) -C "./frontend/" install

.PHONY: build-frontend
build-frontend:  ## Build React Frontend
	$(MAKE) -C "./frontend/" build

.PHONY: start-frontend
start-frontend:  ## Start React Frontend
	$(MAKE) -C "./frontend/" start

.PHONY: install-backend
install-backend:  ## Create virtualenv and install Plone
	$(MAKE) -C "./backend/" build-dev
	$(MAKE) create-site

.PHONY: create-site
create-site: ## Create a Plone site with default content
	$(MAKE) -C "./backend/" create-site

.PHONY: start-backend
start-backend: ## Start Plone Backend
	$(MAKE) -C "./backend/" start

.PHONY: install
install:  ## Install
	@echo "Install Backend & Frontend"
	$(MAKE) install-backend
	$(MAKE) install-frontend

.PHONY: build
build:  ## Build
	@echo "Build"
	$(MAKE) build-backend
	$(MAKE) build-frontend

.PHONY: start
start:  ## Start
	@echo "Starting application"
	$(MAKE) start-backend
	$(MAKE) start-frontend

.PHONY: format
format:  ## Format codebase
	@echo "Format codebase"
	$(MAKE) -C "./backend/" format
	$(MAKE) -C "./frontend/" format

.PHONY: test
test:  ## Test codebase
	@echo "Test codebase"
	$(MAKE) -C "./backend/" test
	$(MAKE) -C "./frontend/" test


.PHONY: build-images
build-images:  ## Build docker images
	@echo "Build"
	$(MAKE) -C "./backend/" build-image
	$(MAKE) -C "./frontend/" build-image

## Docker stack
.PHONY: start-stack
start-stack:  ## Start local stack
	@echo "Start local Docker stack"
	@docker-compose -f devops/stacks/docker-compose-local.yml up -d --build

.PHONY: stop-stack
stop-stack:  ## Stop local stack
	@echo "Stop local Docker stack"
	@docker-compose -f devops/stacks/docker-compose-local.yml down

## Acceptance
.PHONY: build-acceptance-servers
build-acceptance-servers: ## Build Acceptance Servers
	@echo "Build acceptance backend"
	@docker build backend -t ploneorgbr/site-backend:acceptance -f backend/Dockerfile.acceptance
	@echo "Build acceptance frontend"
	@docker build frontend -t ploneorgbr/site-frontend:acceptance -f frontend/Dockerfile

.PHONY: start-acceptance-servers
start-acceptance-servers: build-acceptance-servers ## Start Acceptance Servers
	@echo "Start acceptance backend"
	@docker run --rm -p 55001:55001 --name site-backend-acceptance -d ploneorgbr/site-backend:acceptance
	@echo "Start acceptance frontend"
	@docker run --rm -p 3000:3000 --name site-frontend-acceptance --link site-backend-acceptance:backend -e RAZZLE_API_PATH=http://localhost:55001/plone -e RAZZLE_INTERNAL_API_PATH=http://backend:55001/plone -d ploneorgbr/site-frontend:acceptance

.PHONY: stop-acceptance-servers
stop-acceptance-servers: ## Stop Acceptance Servers
	@echo "Stop acceptance containers"
	@docker stop site-frontend-acceptance
	@docker stop site-backend-acceptance

.PHONY: run-acceptance-tests
run-acceptance-tests: ## Run Acceptance tests
	$(MAKE) start-acceptance-servers
	npx wait-on --httpTimeout 20000 http-get://localhost:55001/plone http://localhost:3000
	$(MAKE) -C "./frontend/" test-acceptance-headless
	$(MAKE) stop-acceptance-servers
