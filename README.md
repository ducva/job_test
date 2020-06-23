# Prerequisites

- Docker
  Check this link for more information: [https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/)

# Run in Development mode

make sure to run `make clean` first, if you run `make test` or `make prod` before

```shell script
make
```

After the process finishes, our application runs at port 5000.


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