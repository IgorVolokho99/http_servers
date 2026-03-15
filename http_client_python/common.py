import time

import argparse
from typing import Any


def cli_args(func):
    def wrapper():
        parser = argparse.ArgumentParser()

        parser.add_argument('--host', default='localhost')
        parser.add_argument('--port', type=int, required=True)
        parser.add_argument('--clients', type=int, default=1)
        parser.add_argument('--requests', type=int, default=1)

        args = parser.parse_args()

        return func(
            host=args.host,
            port=args.port,
            clients=args.clients,
            amount_of_requests=args.requests
        )
    return wrapper


def timed(func: callable) -> callable:
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"Time: {time.perf_counter() - start_time}")
        return result
    return wrapper