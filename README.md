# powerplant-coding-challenge


## Execute the application with Docker

1. Build Docker image:

```bash
docker build -t powerplant .

docker run -p 8888:8888 --name powerplant-app powerplant
```


If you want to run the test, in other terminal run

```bash
docker exec -it powerplant-app bash
```
And inside the container just run

```bash
pytest
```