import httpx

from http_client_python.common import cli_args, timed


def make_requests(amount_of_requests: int, host: str, port: int) -> None:
    url = f"http://{host}:{port}/"
    with httpx.Client() as client:
        for _ in range(amount_of_requests):
            response = client.get(url)


@cli_args
@timed
def main(amount_of_requests: int = 1000, host: str = "127.0.0.1", port: int = 50001, **kwargs:dict) -> None:
    make_requests(amount_of_requests=amount_of_requests, host=host, port=port)


if __name__ == "__main__":
    main()