import asyncio
import time

import aiohttp

from http_client_python.common import cli_args, timed


async def make_request(host: str, port: int) -> None:
    async with aiohttp.ClientSession() as session:
        async with session.get(url=f"http://{host}:{port}/") as response:
            # print(response.status)
            response.status


# @cli_args
# @timed
async def main(amount_of_requests: int = 1000, clients: int = 1, host: str = "127.0.0.1", port: int = 50001, **kwargs:dict) -> None:
    tasks = [asyncio.create_task(make_request("127.0.0.1", 50001)) for _ in range(amount_of_requests)]
    await asyncio.gather(*tasks)
    


if __name__ == "__main__":
    start_time = time.perf_counter()
    asyncio.run(main())
    print(f"Time: {time.perf_counter() - start_time}")