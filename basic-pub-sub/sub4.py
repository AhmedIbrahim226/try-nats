import asyncio
from datetime import datetime, UTC
import json
import nats


NAME="13.14.15.16"
IS_BUSY: bool = False
SUBSERVER_STATUS_SCHE = (lambda: {
    "ip": NAME,
    "is_busy": IS_BUSY
})


async def run_task(data: dict):
    global IS_BUSY

    task_prefix = data["task_prefix"]
    IS_BUSY = True
    print(task_prefix)
    await asyncio.sleep(60)
    IS_BUSY=False


async def main():
    async def close_done():
        print("CLOSED")

    nc = await nats.connect("nats://localhost:4222", closed_cb=close_done, name=NAME)

    async def message_handler(msg):
        print(IS_BUSY)
        subject = msg.subject
        data = msg.data.decode()
        if msg.reply:
            await nc.publish(msg.reply, json.dumps(SUBSERVER_STATUS_SCHE()).encode())
            print(f"Received a message on '{subject}': {data}")
            return

        if not IS_BUSY:
            asyncio.create_task(run_task(json.loads(data)))


    sub = await nc.subscribe(subject="server-link", cb=message_handler)
    await nc.publish("sub-server-registry", NAME.encode())
        
    # await sub.unsubscribe(limit=1)


    await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
