
.PHONY: run test shell migrate makemigrations build up down

run:
	docker compose up

import_countries:
	docker compose run --rm web python manage.py import_countries

test:
	docker exec -it countriesapp-web-1 pytest --tb=short -v

coverage:
	docker exec -it countriesapp-web-1 pytest --cov=countries --tb=short -v
	
shell:
	docker compose run --rm web python manage.py shell

migrate:
	docker compose run --rm web python manage.py migrate

makemigrations:
	docker compose run --rm web python manage.py makemigrations

build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down
