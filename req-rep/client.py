import os
import asyncio


import nats
from nats.aio.client import Client as Nats
from nats.errors import TimeoutError, NoRespondersError

servers = os.environ.get("NATS_URL", "nats://localhost:4222").split(",")


class MyNats(Nats):
    def __init__(self):
        self.client_name = "C1"
        super().__init__()


async def main():
    nc = MyNats()
    await nc.connect(servers=servers)

    # sub = await nc.subscribe("greet.*", cb=greet_handler)
    # await asyncio.Future()

    # sub = await nc.subscribe("greet.*")
    sub = await nc.subscribe("check-servers-health")

    async for msg in sub.messages:
        response = f"hello, {msg.subject}"
        if msg.reply:
            await msg.respond(f"Response from {nc.client_name}".encode())
        print(msg.data.decode())


async def greet_handler(msg):
    # print(msg)
    # name = msg.subject[6:]
    response = f"hello, {msg.subject}"
    print(response)
    if msg.reply:
        await msg.respond(response.encode("utf8"))
    print(msg.data)


if __name__ == "__main__":
    asyncio.run(main())
