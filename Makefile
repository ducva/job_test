.PHONY: all dev test prod clean

all: dev

.env.test:
	sed "s/DB_NAME=flaskdb/DB_NAME=flaskdb_test/g" .env.example > .env.test

.env:
	sed "s/DB_NAME=flaskdb/DB_NAME=flaskdb_prod/g" .env.example > .env

.env.dev:
	sed "s/DB_NAME=flaskdb/DB_NAME=flaskdb_dev/g" .env.example > .env.dev

dev: .env.dev
	docker-compose --env-file .env.dev  up -d
	docker-compose restart flask
	docker-compose logs -f flask


test: .env.test
	docker-compose --env-file .env.test -f docker-compose.yml -f docker-compose.test.yml up -d --force-recreate
	docker-compose logs -f flask


prod: .env
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --force-recreate
	docker-compose logs -f


clean:
	docker-compose down -v

