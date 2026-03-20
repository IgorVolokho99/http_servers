import asyncio
import time

try:
    import uvloop
except ImportError:
    uvloop = None


HOST = "127.0.0.1"
PORT = 50001
PATH = "/"

TOTAL_REQUESTS = 10_000
CONCURRENCY = 128
REQUEST_TIMEOUT = 5.0

REQUEST = (
    f"GET {PATH} HTTP/1.1\r\n"
    f"Host: {HOST}:{PORT}\r\n"
    f"Connection: close\r\n"
    f"\r\n"
).encode("ascii")


async def one_request() -> bool:
    reader = None
    writer = None

    try:
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(HOST, PORT),
            timeout=REQUEST_TIMEOUT,
        )

        writer.write(REQUEST)
        await writer.drain()

        status_line = await asyncio.wait_for(reader.readline(), timeout=REQUEST_TIMEOUT)
        if not status_line.startswith(b"HTTP/1.1 200") and not status_line.startswith(b"HTTP/1.0 200"):
            return False

        while True:
            line = await asyncio.wait_for(reader.readline(), timeout=REQUEST_TIMEOUT)
            if line in (b"\r\n", b""):
                break

        await asyncio.wait_for(reader.read(), timeout=REQUEST_TIMEOUT)
        return True

    except Exception:
        return False

    finally:
        if writer is not None:
            writer.close()
            try:
                await writer.wait_closed()
            except Exception:
                pass


async def worker(amount: int) -> tuple[int, int]:
    ok = 0
    err = 0

    for _ in range(amount):
        if await one_request():
            ok += 1
        else:
            err += 1

    return ok, err


async def main() -> None:
    per_worker = TOTAL_REQUESTS // CONCURRENCY
    extra = TOTAL_REQUESTS % CONCURRENCY

    tasks = []
    start = time.perf_counter()

    for i in range(CONCURRENCY):
        count = per_worker + (1 if i < extra else 0)
        if count > 0:
            tasks.append(asyncio.create_task(worker(count)))

    results = await asyncio.gather(*tasks)
    elapsed = time.perf_counter() - start

    ok = sum(x[0] for x in results)
    err = sum(x[1] for x in results)

    print(f"URL: http://{HOST}:{PORT}{PATH}")
    print(f"Total requests: {TOTAL_REQUESTS}")
    print(f"Concurrency: {CONCURRENCY}")
    print(f"Success: {ok}")
    print(f"Errors: {err}")
    print(f"Elapsed: {elapsed:.4f} sec")
    print(f"RPS: {ok / elapsed:.2f}")


if __name__ == "__main__":
    if uvloop is not None:
        with asyncio.Runner(loop_factory=uvloop.new_event_loop) as runner:
            runner.run(main())
    else:
        asyncio.run(main())