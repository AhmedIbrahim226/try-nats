import asyncio
import nats


async def main():
    async def closed_cb():
        print("CLOSED")

    # Connect to the server
    nc = await nats.connect("nats://localhost:4222", closed_cb=closed_cb)

    # Publish a message to the 'greetings' subject
    for i in range(100):
        message = f"Hello, World! #{i}"
        await nc.publish("greetings", message.encode())
        print(f"Published: {message}")
        # await asyncio.sleep(1)  # Wait a second between messages

    # Gracefully close the connection
    await nc.flush()
    await nc.drain()


if __name__ == "__main__":
    asyncio.run(main())
