setup:
	cp .env.example .env


build:
	docker-compose build


dev:
	docker-compose up -d
	docker-compose logs -f flask

clean:
	docker-compose stop
	docker-compose rm -vf
	docker volume prune --force
