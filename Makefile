define run_docker_cmd
	docker compose run --rm \
		app \
		"$(1)"
endef

.PHONY: build start shell stop test

build:
	docker compose build

start:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d

shell: start
	docker compose exec app bash

stop:
	docker compose down

test:
	$(call run_docker_cmd,pytest)
