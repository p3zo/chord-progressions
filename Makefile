define run_docker_cmd
	docker-compose run --rm \
		app \
		"$(1)"
endef

.PHONY: build bump clean dev generate shell stop test

build:
	@echo "Building image:"
	docker-compose build

clean:
	@echo "Cleaning up artifacts:"
	rm -rf dist

dev:
	@echo "Starting container(s) in dev mode:"
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d

format:
	@echo "Formatting:"
	$(call run_docker_cmd,isort chord_progressions tests && black chord_progressions tests)

generate: dev
	@echo "Generating a progression locally:"
	$(call run_docker_cmd,run.sh)

shell: dev
	@echo "Getting a shell inside the container:"
	docker-compose exec app bash

stop:
	@echo "Bringing Docker down:"
	docker-compose down

test: build
	@echo "Running tests:"
	$(call run_docker_cmd,pytest)
	docker-compose down
