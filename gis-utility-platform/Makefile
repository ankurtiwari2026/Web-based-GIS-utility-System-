SHELL := /usr/bin/bash

.PHONY: dev build up down logs psql

dev:
	docker compose up -d --build

build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down -v

logs:
	docker compose logs -f --tail=100

psql:
	docker compose exec db psql -U postgres -d gis | cat

