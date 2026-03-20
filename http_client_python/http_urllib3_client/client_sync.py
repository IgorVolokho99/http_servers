import time
import urllib3

from http_client_python.common import cli_args, timed

http = urllib3.PoolManager()

def make_request(host:str, port:int) -> None:
    response = http.request("GET", f"http://{host}:{port}")
    #print(response.data.decode("utf-8"))    


@cli_args
@timed
def main(amount_of_requests: int = 1000, clients: int = 1, host: str = "127.0.0.1", port: int = 50001, **kwargs:dict) -> None:
    for _ in range(amount_of_requests):
        make_request(host, port)


if __name__ == "__main__":
    main()
