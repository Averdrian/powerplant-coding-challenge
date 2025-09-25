# powerplant-coding-challenge


## Ejecutar la aplicación con Docker

1. Construir la imagen Docker:

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