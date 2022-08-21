black:
	black . --line-length 120

prod_up:
	docker compose -f docker-compose-databases-prod.yml -f docker-compose.yml up -d

prod_down:
	docker compose -f docker-compose-databases-prod.yml -f docker-compose.yml down

dev_up:
	docker compose -f docker-compose-databases.yml -f docker-compose-dev.yml pg_auth up -d

dev_down:
	docker compose -f docker-compose-databases.yml -f docker-compose-dev.yml down

tests_up:
	docker compose -f tests/functional/docker-compose.yml up

tests_down:
	docker compose -f tests/functional/docker-compose.yml down

auth_debug:
	flask --app auth/src/Auth.app --debug run