clean:
	docker-compose stop
	docker-compose rm -vf
	docker volume prune --force
