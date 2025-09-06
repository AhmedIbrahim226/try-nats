import asyncio

from nats.aio.client import Client as Nats
from nats.js.api import ConsumerConfig


async def main():
    nc = Nats()
    await nc.connect("nats://localhost:4222")
    js = nc.jetstream()

    # Create an EPHEMERAL consumer by not providing a 'durable' name.
    # The server will generate a random name for it.
    sub = await js.subscribe(
        "commands.ephemeral", cb=message_handler, config=ConsumerConfig(name="Client1")
    )
    print(f"✅ Connected! ephemeral consumer is active.")
    print(f"ℹ️  Server-assigned consumer name: {sub._consumer}")

    await asyncio.Future()
    # Disconnect gracefully
    # print("⏹️  Client disconnecting now.")
    # await nc.drain()


async def message_handler(msg):
    print(f"📨 Received: {msg}")
    await msg.ack()
    print(f"📨 Received: {msg}")
    print("------------------------------------")


if __name__ == "__main__":
    asyncio.run(main())
    # When this script stops, the consumer is automatically deleted.
