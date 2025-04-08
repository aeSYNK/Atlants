# Atlant Backend

The service uses the following technologies:


- `python ^3.13`
- `poetry ==2.1.2`
- `fastapi ^0.115.12`
- `redis ^5.2.1,<6.0.0`


## How to run local environment via docker
```sh
$ git clone https://github.com/aeSYNK/Atlants.git
$ docker-compose -f docker-compose.yml up --build -d
$ docker-compose logs # For see containers logs.
```

## How to run local environment via local machine

```sh
$ docker run -d --name redis -p 6379:6379 -v redis_data:/data
$ activate venv
$ pip install poetry
$ cd app
$ poetry install
$ fastapi dev main.py
```
