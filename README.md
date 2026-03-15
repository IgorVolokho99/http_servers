## Server

```
python3 http_server_python/flask_server/main.py
```

## GuniCorn

```
gunicorn http_server_python.flask_server.main:app -w 4 --threads 1 -b 0.0.0.0:50001
```

## GuniCorn nice res:

```
gunicorn http_server_python.flask_server.main:app -w 8 --threads 1 -b 0.0.0.0:50001
```


## Clients requests
```sync
python3 -m http_client_python.requests_client.client_sync --requests 1000 --clients 1
```

```thread
python3 -m http_client_python.requests_client.client_multithreading --requests 5000 --clients 1
```

```proccess
python3 -m http_client_python.requests_client.client_multiproccessing --requests 250 --clients 4
```

## Clients httpx
```sync
python -m http_client_python.httpx_client.client_sync --requests 1000 --port 50001
```

```thread
python -m http_client_python.httpx_client.client_multithreading --requests 1000 --port 50001
```

```process
python -m http_client_python.httpx_client.client_multiprocessing --requests 1000 --port 50001
```