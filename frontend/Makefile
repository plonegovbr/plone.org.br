### Defensive settings for make:
#     https://tech.davis-hansson.com/p/make/
SHELL:=bash
.ONESHELL:
.SHELLFLAGS:=-xeu -o pipefail -O inherit_errexit -c
.SILENT:
.DELETE_ON_ERROR:
MAKEFLAGS+=--warn-undefined-variables
MAKEFLAGS+=--no-builtin-rules
IMAGE_NAME=ghcr.io/plonegovbr/ploneorgbr-frontend
IMAGE_TAG=latest

NODEBIN = ./node_modules/.bin

# Add the following 'help' target to your Makefile
# And add help text after each target name starting with '\#\#'
.PHONY: help
help: ## This help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: clean
clean: ## Clean up the installation
	@echo "Clean up node_modules"
	rm -Rf node_modules .yarn/cache omelette cache build

.PHONY: install
install: ## Install the frontend
	@echo "Install frontend"
	corepack enable
	yarn install  --network-timeout 1000000

.PHONY: build
build: install ## Build the frontend
	@echo "Build Frontend"
	yarn build

.PHONY: start
start: ## Start Frontend
	yarn start

.PHONY: format-prettier
format-prettier: ## Format Code with Prettier
	yarn run prettier:fix

.PHONY: format-stylelint
format-stylelint: ## Format Code with Stylelint
	yarn run stylelint:fix

.PHONY: format-lint
format-lint: ## Format Code with Lint
	yarn run lint:fix

.PHONY: format
format: format-prettier format-stylelint format-lint ## Format the codebase according to our standards

.PHONY: lint
lint: ## Lint codebase
	yarn lint
	yarn prettier

.PHONY: preinstall
preinstall:
	if [ -f $$(pwd)/mrs.developer.json ]; then if [ -f $$(pwd)/node_modules/.bin/missdev ]; then yarn develop; else yarn develop:npx; fi; fi

.PHONY: omelette
omelette:
	if [ ! -d omelette ]; then ln -sf node_modules/@plone/volto omelette; fi

.PHONY: i18n
i18n: ## Sync i18n
	yarn i18n

.PHONY: i18n-ci
i18n-ci: ## Check if i18n is not synced
	yarn i18n && git diff -G'^[^\"POT]' --exit-code

.PHONY: test
test: ## Run tests
	yarn run test

.PHONY: test-ci
test-ci: ## Run tests
	yarn run test:ci

.PHONY: build-image
build-image:  ## Build Docker Image
	@docker build . -t $(IMAGE_NAME):$(IMAGE_TAG) -f Dockerfile


# Acceptance tests

.PHONY: test-acceptance
test-acceptance: ## Start Core Cypress Acceptance Tests
	NODE_ENV=production CYPRESS_API=plone $(NODEBIN)/cypress open

.PHONY: test-acceptance-headless
test-acceptance-headless: ## Start Core Cypress Acceptance Tests in headless mode
	NODE_ENV=production CYPRESS_API=plone $(NODEBIN)/cypress run
