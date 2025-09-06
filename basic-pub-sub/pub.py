import asyncio
import json
import re
from pprint import pprint

import aiohttp
import nats


async def main():
    async def closed_cb():
        print("CLOSED")

    # Connect to the server
    nc = await nats.connect("nats://localhost:4222", closed_cb=closed_cb)

    # Publish a message to the 'greetings' subject
    # for i in range(100):
    message = f"Hello, World! #Sub-Servers"
    await nc.publish("greetings1", message.encode())
    print(f"Published: {message}")
    # await asyncio.sleep(5)  # Wait a second between messages



    async with aiohttp.ClientSession(base_url="http://localhost:8222") as session:
        while True:
            async with session.get('/connz?subs=true&state=open') as response:
                print("Status:", response.status)
                body = await response.json()
                connections = body["connections"]
                # pprint(connections)
                print("------------------------")
                sub_servers = list(filter(lambda i: re.search(r"\bsub_server\w*\b", i.get("name", "")) and "greetings1" in i["subscriptions_list"] , connections))
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
