setup:
	cp .env.example .env


build:
	docker-compose build


dev:
	docker-compose --env-file dev.env  up -d
	docker-compose logs -f flask


test:
	docker-compose --env-file test.env -f docker-compose.yml -f docker-compose.test.yml up -d --force-recreate
	docker-compose logs -f flask


prod:
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --force-recreate
	docker-compose logs -f

clean:
	docker-compose stop
	docker-compose rm -vf
	docker volume prune --force
