import time
import asyncio
import httpx
from datetime import datetime
from fastapi import FastAPI

app = FastAPI()

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] {msg}")

def cpu_work():
    x = 0
    for i in range(10_000_000):
        x += i * i
    return x

# ─────────────────────────────────────────
# SCENARIO 1: def (sync) route
# ─────────────────────────────────────────
@app.get("/sync")
def sync_route():
    log("sync | started")
    cpu_work()
    log("sync | rest of code done")
    time.sleep(5)
    log("sync | db call done (5s)")
    return {"status": "sync done"}

# ─────────────────────────────────────────
# SCENARIO 2: async def route
# ─────────────────────────────────────────
@app.get("/async")
async def async_route():
    log("async | started")
    cpu_work()                     # blocks event loop (rest of code)
    log("async | rest of code done")
    await asyncio.sleep(5)         # releases event loop (db call)
    log("async | db call done (5s)")
    return {"status": "async done"}

# ─────────────────────────────────────────
# Test runner — fires 2 simultaneous requests
# ─────────────────────────────────────────
async def fire_two_requests(url: str, label: str):
    print(f"\n{'='*50}")
    print(f"Testing: {label}  →  {url}")
    print(f"{'='*50}")
    start = time.time()

    async with httpx.AsyncClient(timeout=60) as client:
        results = await asyncio.gather(
            client.get(url),
            client.get(url),
        )

    elapsed = time.time() - start
    for i, r in enumerate(results):
        print(f"  Request {i+1}: {r.json()}")
    print(f"  Total wall time: {elapsed:.2f}s")

if __name__ == "__main__":
    import uvicorn
    import multiprocessing

    def run_server():
        uvicorn.run(app, host="127.0.0.1", port=8000, log_level="warning")

    server = multiprocessing.Process(target=run_server)
    server.start()
    time.sleep(1)

    async def run_tests():
        await fire_two_requests("http://127.0.0.1:8000/sync",  "def (sync) route")
        await fire_two_requests("http://127.0.0.1:8000/async", "async def route")

    asyncio.run(run_tests())
    server.terminate()
    server.join()