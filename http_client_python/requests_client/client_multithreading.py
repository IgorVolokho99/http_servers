import time
from threading import Thread

import requests

from http_client_python.common import cli_args, timed

def make_request(amount_of_requests):
    for _ in range(amount_of_requests):
        response = requests.get("http://127.0.0.1:50001")

@timed
@cli_args
def main(amount_of_requests: int = 1000, clients: int = 1, host: str = "127.0.0.1", port: int = 50001, **kwargs:dict) -> None:
    threads = [Thread(target=make_request, args=(amount_of_requests, )) for _ in range(clients)]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()
