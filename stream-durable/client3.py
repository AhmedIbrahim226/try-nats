import asyncio
from nats.aio.client import Client as NATS
from nats.js.api import ConsumerConfig

STREAM_NAME = "broadcast_commands"
SUBJECT = "commands.important"
CONSUMER_NAME = "sub-server-3"


async def main():
    nc = NATS()
    await nc.connect("nats://localhost:4222")
    js = nc.jetstream()

    # Create a DURABLE pull consumer
    await js.add_consumer(
        STREAM_NAME,
        config=ConsumerConfig(
            durable_name=CONSUMER_NAME,
            ack_wait=30,  # Wait 30s for an ack before redelivering
        ),
    )

    # Bind to the consumer
    sub = await js.pull_subscribe(SUBJECT, durable=CONSUMER_NAME)

    print(f"Subscriber {CONSUMER_NAME} is reading from stream '{STREAM_NAME}'...")

    try:
        while True:
            # Fetch messages in batches
            msgs = await sub.fetch(5, timeout=5)
            for msg in msgs:
                print(f"Processing: {msg.data.decode()}")
                # Simulate work - might fail sometimes!
                await asyncio.sleep(1)
                # IMPORTANT: Acknowledge successful processing
                await msg.ack()
                print(f"✅ Acknowledged message sequence {msg}")

    except asyncio.TimeoutError:
        print("No messages. Fetching again...")
        # In a real service, you would loop here instead of exiting.
    finally:
        await nc.drain()


if __name__ == "__main__":
    asyncio.run(main())
