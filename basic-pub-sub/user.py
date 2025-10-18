import asyncio
from time import sleep

from pub import init_nats_conn
from asgiref.sync import async_to_sync

# nc = async_to_sync(init_nats_conn)()


async def main ():
    nc = await init_nats_conn()

    # while True:
    #     inp = input("Input Message: ")
    for i in range(30):
        await nc.publish("manage-tasks", f"{"mohamed"}".encode())
        # await asyncio.sleep(0.5)


if __name__ == '__main__':
    asyncio.run(main())