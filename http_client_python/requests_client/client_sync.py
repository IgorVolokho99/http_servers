import time

import requests

from http_client_python.common import cmd_args, timed

def make_request() -> None:
    response = requests.get("http://127.0.0.1:50001")

@cmd_args
@timed
def main(amount_of_requests: int = 1_000, clients: int=1) -> None:
    for _ in range(amount_of_requests):
        make_request()


if __name__ == "__main__":
    main()
