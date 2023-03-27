.SILENT:
.DEFAULT_GOAL := help

PROJECT := Space Test App

## Installs a development environment
install: deploy

## Composes project using docker-compose
deploy:
	docker-compose -f deployments/docker-compose.yml build
	docker-compose -f deployments/docker-compose.yml down -v
	docker-compose -f deployments/docker-compose.yml up --force-recreate

## Prints help message
help:
	printf "\n${COLOR_YELLOW}${PROJECT}\n------\n${COLOR_RESET}"
	awk '/^[a-zA-Z\-\_0-9\.%]+:/ { \
		helpMessage = match(lastLine, /^## (.*)/); \
		if (helpMessage) { \
			helpCommand = substr($$1, 0, index($$1, ":")); \
			helpMessage = substr(lastLine, RSTART + 3, RLENGTH); \
			printf "${COLOR_COMMAND}$$ make %s${COLOR_RESET} %s\n", helpCommand, helpMessage; \
		} \
	} \
	{ lastLine = $$0 }' $(MAKEFILE_LIST) | sort
	printf "\n"