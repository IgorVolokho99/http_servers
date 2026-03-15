from threading import Thread

import httpx

from http_client_python.common import cli_args, timed


def make_requests(amount_of_requests: int, host: str, port: int) -> None:
    url = f"http://{host}:{port}/"
    with httpx.Client() as client:
        for _ in range(amount_of_requests):
            response = client.get(url)


@cli_args
@timed
def main(amount_of_requests: int = 1000, clients: int = 1, host: str = "127.0.0.1", port: int = 50001, **kwargs:dict) -> None:

    threads: list[Thread] = [Thread(target=make_requests, args=(amount_of_requests, host, port)) for _ in range(clients)]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()
