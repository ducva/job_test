# Prerequisites

- Docker
  Check this link for more information: [https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/)

# Run in Development mode

make sure to run `make clean` first, if you run `make test` or `make prod` before

```shell script
make
```

After the process finishes, you can:
- access API's spec at: http://localhost:8082
- call API at: http://localhost:5000



# Run Tests

make sure to run `make clean` first, if you run `make dev` (or `make`) or `make prod` before

```shell script
make test
```

# Run in Production mode

make sure to run `make clean` first, if you run `make test` or `make dev` (or `make`) before

```shell script
make prod
```

After the process finishes, API is running at http://localhost:8080


# Todos

- Run in dev mode without wsgi
