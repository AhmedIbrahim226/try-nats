import asyncio
import json
import re
from pprint import pprint

import aiohttp
import nats


async def closed_cb():
    print("CLOSED")


async def init_nats_conn():
    # Connect to the server
    nc = await nats.connect("nats://localhost:4222", closed_cb=closed_cb)
    return nc

async def main():

    nc = await init_nats_conn()
    message = f"Hello, World! #Sub-Servers"
    await nc.publish("sub-server-health", message.encode())
    print(f"Published: {message}")


    async with aiohttp.ClientSession(base_url="http://localhost:8222") as session:
        while True:
            async with session.get('/connz?subs=true&state=open') as response:
                print("Status:", response.status)
                body = await response.json()
                connections = body["connections"]
                # pprint(connections)
                print("------------------------")
                sub_servers = list(filter(lambda i: re.search(r"\bsub_server\w*\b", i.get("name", "")) and "sub-server-health" in i["subscriptions_list"] , connections))
                for sub_server_info in sub_servers:
                    print(sub_server_info["name"])
                print("Content-type:", response.headers['content-type'])
                print("------------------------")


            await asyncio.sleep(3)



    # Gracefully close the connection
    # await nc.flush()
    # await nc.drain()
    await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
