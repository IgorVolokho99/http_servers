import asyncio
import math
import time
from dataclasses import dataclass

import aiohttp

try:
    import uvloop
except ImportError:
    uvloop = None


@dataclass(slots=True)
class BenchmarkResult:
    total_requests: int
    concurrency: int
    success: int
    errors: int
    elapsed_sec: float

    @property
    def rps(self) -> float:
        if self.elapsed_sec == 0:
            return 0.0
        return self.success / self.elapsed_sec


async def worker(
    worker_id: int,
    requests_to_make: int,
    session: aiohttp.ClientSession,
    url: str,
) -> tuple[int, int]:
    success = 0
    errors = 0

    for _ in range(requests_to_make):
        try:
            async with session.get(url) as response:
                # Важно дочитать тело ответа, чтобы соединение корректно
                # вернулось в пул и переиспользовалось.
                await response.read()

                if response.status == 200:
                    success += 1
                else:
                    errors += 1

        except Exception:
            errors += 1

    return success, errors


async def run_benchmark(
    url: str,
    total_requests: int = 100_000,
    concurrency: int = 1000,
    connect_timeout: float = 5.0,
    read_timeout: float = 30.0,
    warmup_requests: int = 1000,
) -> BenchmarkResult:
    if concurrency <= 0:
        raise ValueError("concurrency must be > 0")

    timeout = aiohttp.ClientTimeout(
        total=None,
        connect=connect_timeout,
        sock_connect=connect_timeout,
        sock_read=read_timeout,
    )

    connector = aiohttp.TCPConnector(
        # Ограничиваем пул именно нашим concurrency.
        # Это обычно лучше, чем безлимит, если ты осознанно задаёшь нагрузку.
        limit=concurrency,
        limit_per_host=concurrency,

        # Для localhost DNS почти не важен, но пусть кэшируется.
        ttl_dns_cache=300,

        # SSL не нужен для http://127.0.0.1...
        ssl=False,

        # Для бенча лишние проверки/очистки нам не нужны.
        enable_cleanup_closed=False,
    )

    async with aiohttp.ClientSession(
        connector=connector,
        timeout=timeout,
        raise_for_status=False,
        auto_decompress=False,
        trust_env=False,
        cookie_jar=aiohttp.DummyCookieJar(),
        read_bufsize=2**16,
    ) as session:
        # Небольшой прогрев
        for _ in range(warmup_requests):
            async with session.get(url) as response:
                await response.read()

        per_worker = total_requests // concurrency
        remainder = total_requests % concurrency

        tasks = []
        start = time.perf_counter()

        for i in range(concurrency):
            count = per_worker + (1 if i < remainder else 0)
            if count == 0:
                continue
            tasks.append(asyncio.create_task(worker(i, count, session, url)))

        results = await asyncio.gather(*tasks)
        elapsed = time.perf_counter() - start

    success = sum(s for s, _ in results)
    errors = sum(e for _, e in results)

    return BenchmarkResult(
        total_requests=total_requests,
        concurrency=concurrency,
        success=success,
        errors=errors,
        elapsed_sec=elapsed,
    )


def main() -> None:
    url = "http://127.0.0.1:50001/"
    total_requests = 10_000
    concurrency = 64

    async def runner() -> None:
        result = await run_benchmark(
            url=url,
            total_requests=total_requests,
            concurrency=concurrency,
            warmup_requests=1000,
        )

        print(f"URL: {url}")
        print(f"Total requests: {result.total_requests}")
        print(f"Concurrency: {result.concurrency}")
        print(f"Success: {result.success}")
        print(f"Errors: {result.errors}")
        print(f"Elapsed: {result.elapsed_sec:.4f} sec")
        print(f"RPS: {result.rps:.2f}")

    if uvloop is not None:
        with asyncio.Runner(loop_factory=uvloop.new_event_loop) as runner_obj:
            runner_obj.run(runner())
    else:
        asyncio.run(runner())

if __name__ == "__main__":
    main()