import time
from multiprocessing import Process

from http_client_python.common import cli_args, timed

import urllib3

http = urllib3.PoolManager()

def make_request(amount_of_requests:int, host:str, port:int) -> None:
    for _ in range(amount_of_requests):    
        response = http.request("GET", f"http://{host}:{port}")


@cli_args
@timed
def main(amount_of_requests: int = 1000, clients: int = 1, host: str = "127.0.0.1", port: int = 50001, **kwargs:dict) -> None:
    
    threads = [Process(target=make_request, args=(amount_of_requests, host, port)) for _ in range(clients)]
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()



if __name__ == "__main__":
    main()
