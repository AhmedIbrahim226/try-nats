import os
import asyncio


import nats
from nats.errors import TimeoutError, NoRespondersError

servers = os.environ.get("NATS_URL", "nats://localhost:4222").split(",")


async def main():

    nc = await nats.connect(servers=servers)

    # await nc.publish("greet.any", b"AnyAhmed")
    # rep = await nc.request("greet.joe", b'', timeout=0.5)
    # print(f"{rep.data}")
    #
    #
    # rep = await nc.request("greet.sue", b'', timeout=0.5)
    # print(f"{rep.data}")
    #
    #
    # rep = await nc.request("greet.bob", b'', timeout=0.5)
    # print(f"{rep.data}")

    while True:
        try:
            rep = await nc.request("check-servers-health", b"", timeout=0.5)
            print(f"{rep.data}")
        except NoRespondersError:
            print("no responders")
        await asyncio.sleep(0.1)

    # try:
    #     rep = await nc.request("greet.joe", b'', timeout=5)
    #     print(rep.data)
    # except NoRespondersError:
    #     print("no responders")

    await nc.drain()
    await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
