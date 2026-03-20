import time
import http.client

from http_client_python.common import cli_args, timed

def make_request(host:str, port:int) -> None:
    conn = http.client.HTTPConnection(host, port=port, timeout=10)
    conn.request("GET", "/")
    response = conn.getresponse()
    response.read()
    conn.close()

@cli_args
@timed
def main(amount_of_requests: int = 1000, clients: int = 1, host: str = "127.0.0.1", port: int = 50001, **kwargs:dict) -> None:
    for _ in range(amount_of_requests):
        make_request(host, port)


if __name__ == "__main__":
    main()
