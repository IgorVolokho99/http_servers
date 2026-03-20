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


## Clients http.client

```sync
python3 -m http_client_python.http_client_client.client_sync --requests 1000 --clients 1 --port 50001
```

```sync_mod
python3 -m http_client_python.http_client_client.client_sync_mod --requests 1000 --clients 1 --port 50001
```

```thread
python3 -m http_client_python.http_client_client.client_multithreading --requests 1000 --clients 1 --port 50001
```


Самый быстрый
```process
python3 -m http_client_python.http_client_client.client_multiprocessing --requests 1000 --clients 1 --port 50001
```


## Clients urllib3

```sync
python3 -m http_client_python.http_urllib3_client.client_sync --requests 1000 --port 50001
```

```threading
python3 -m http_client_python.http_urllib3_client.client_multithreding --requests 1000 --clients 1 --port 50001
```

```process
python3 -m http_client_python.http_urllib3_client.client_multiprocessing --requests 1000 --clients 1 --port 50001
```