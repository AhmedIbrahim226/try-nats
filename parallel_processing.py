import asyncio
import os
import random
from datetime import datetime, UTC

import nats


async def main():

    nats_url = os.getenv("NATS_URL", "nats://localhost:4222")

    client = await nats.connect(nats_url)

    sub = await client.subscribe("greet.*", max_msgs=50)

    for i in range(50, 0, -1):
        await client.publish("greet.joe", payload=f"{i}".encode())
        print("done")

    semaphore = asyncio.Semaphore(25)

    async def process_message(message):
        # async with semaphore:
        #     await asyncio.sleep(random.uniform(0, 0.5))
        #     print("received at", datetime.now(tz=UTC))
        await asyncio.sleep(int(message.data.decode()))
        print(f"received message: {message.data.decode()!r}")

    # async for msg in sub.messages:
    #     await asyncio.sleep(int(msg.data.decode()))
    #     print(f"received message: {msg.data.decode()!r}")

    await asyncio.gather(*[process_message(msg) async for msg in sub.messages])


if __name__ == "__main__":
    asyncio.run(main())
