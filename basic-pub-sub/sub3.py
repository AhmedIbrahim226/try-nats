import asyncio
from datetime import datetime, UTC
import json
import nats

NAME="9.10.11.12"
IS_BUSY: bool = False
SUBSERVER_STATUS_SCHE = {
    "ip": NAME,
    "is_busy": IS_BUSY
}

async def main():
    async def close_done():
        print("CLOSED")
    
    nc = await nats.connect("nats://localhost:4222", closed_cb=close_done, name=NAME)

    async def message_handler(msg):
        subject = msg.subject
        data = msg.data.decode()
        if msg.reply:
            await nc.publish(msg.reply, json.dumps(SUBSERVER_STATUS_SCHE).encode())
        print(f"Received a message on '{subject}': {data}")


    async def task_handler(msg):
        await asyncio.sleep(3)
        print(datetime.now(tz=UTC), 5 * f"{msg.data.decode()}")

    sub = await nc.subscribe(subject="server-link", cb=message_handler)
    await nc.publish("sub-server-registry", NAME.encode())

    # await sub.unsubscribe(limit=1)


    await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
