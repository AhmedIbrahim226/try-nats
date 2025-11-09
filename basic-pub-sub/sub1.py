import asyncio
import nats
from datetime import datetime, UTC


async def main():
    async def disconnected_cb():
        print("DISCONNECTED")

    async def closed_cb():
        print("CLOSED")

    nc = await nats.connect("nats://localhost:4222", closed_cb=closed_cb, disconnected_cb=disconnected_cb, name="1.2.3.4")

    async def message_handler(msg):
        subject = msg.subject
        data = msg.data.decode()
        print(f"Received a message on '{subject}': {data}")

    async def task_handler(msg):
        await asyncio.sleep(3)
        print(datetime.now(tz=UTC), 5 * f"{msg.data.decode()}")

    sub = await nc.subscribe(subject="server-link", cb=message_handler)

    # await sub.unsubscribe(limit=1)

    await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
