import asyncio
from datetime import datetime

import nats


async def main():
    async def close_done():
        print("CLOSED")

    nc = await nats.connect("nats://localhost:4222", closed_cb=close_done, name="sub_server_5")

    async def message_handler(msg):
        subject = msg.subject
        data = msg.data.decode()
        print(f"Received a message on '{subject}': {data}")

    async def task_handler(msg):
        await asyncio.sleep(10)
        print(datetime.utcnow(), 5 * f"{msg.data.decode()}")

    sub = await nc.subscribe(subject="sub-server-health", cb=message_handler)

    worker_sub = await nc.subscribe(subject="manage-tasks", queue="manage-tasks-worker", cb=task_handler)
    print(f"Subscribed to 'manage-tasks'. Waiting for messages...")
    # await sub.unsubscribe(limit=1)

    await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
