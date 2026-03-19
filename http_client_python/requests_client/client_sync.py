import time

import requests

from http_client_python.common import cli_args, timed

def make_request() -> None:
    response = requests.get("http://127.0.0.1:50001")

@cli_args
@timed
def main(amount_of_requests: int = 1000, clients: int = 1, host: str = "127.0.0.1", port: int = 50001, **kwargs:dict) -> None:
    for _ in range(amount_of_requests):
        make_request()


if __name__ == "__main__":
    main()
