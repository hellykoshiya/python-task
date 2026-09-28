import time
import requests
import asyncio
import httpx

urls = [
    "https://httpbin.org/delay/1",
    "https://httpbin.org/delay/1",
    "https://httpbin.org/delay/1",
    "https://httpbin.org/delay/1",
    "https://httpbin.org/delay/1",
]


# -------------------------
# 1. Normal requests
# -------------------------
def normal_requests():
    start = time.perf_counter()  #is useful for timing because it is designed for measuring durations.

    for url in urls:
        response = requests.get(url)
        print(f"Status: {response.status_code}")

    end = time.perf_counter()

    print(f"\nNormal requests time: {end - start:.2f} seconds")


# -------------------------
# 2. Async HTTPX
# -------------------------
async def async_requests():
    start = time.perf_counter()

    async with httpx.AsyncClient() as client:
        tasks = [
            client.get(url)
            for url in urls
        ]

        responses = await asyncio.gather(*tasks)  #It allows multiple async operations to be handled together.

        for response in responses:
            print(f"Status: {response.status_code}")

    end = time.perf_counter()

    print(f"\nAsync HTTPX time: {end - start:.2f} seconds")


# Run both
normal_requests()

asyncio.run(async_requests())  #Instead, asyncio.run() starts an event loop and runs your asynchronous function.

# | Code                  | Meaning                                         |
# | --------------------- | ----------------------------------------------- |
# | `requests.get()`      | Normal/synchronous HTTP request                 |
# | `httpx.AsyncClient()` | Asynchronous HTTP client                        |
# | `async def`           | Defines an async function                       |
# | `await`               | Wait for async operation                        |
# | `asyncio.gather()`    | Run/wait for multiple async operations together |
