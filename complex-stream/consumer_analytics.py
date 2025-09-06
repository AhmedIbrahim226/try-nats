# consumer_analytics.py
import asyncio
from nats.aio.client import Client as NATS
from common import STREAM_NAME
import random


async def main():
    nc = await NATS.connect("nats://localhost:4222")
    js = nc.jetstream()

    consumer_name = "analytics-service"
    print(f"Starting {consumer_name}...")

    # Create a consumer
    await js.add_consumer(
        STREAM_NAME,
        config=ConsumerConfig(
            durable_name=consumer_name,
            # Let's sample only 20% of events for analytics
            # We do this in our code, not in the filter.
        ),
    )
    sub = await js.pull_subscribe("orders.>", durable=consumer_name)

    SAMPLE_RATE = 0.2  # Process only 20% of messages
    BATCH_SIZE = 5

    print(f"✅ {consumer_name} subscribed. Sampling {SAMPLE_RATE*100}% of events...")

    try:
        while True:
            # Get a batch of messages
            msgs = await sub.fetch(BATCH_SIZE, timeout=10)
            batch_to_process = []

            for msg in msgs:
                # Sample the messages
                if random.random() <= SAMPLE_RATE:
                    batch_to_process.append(msg)
                else:
                    # Ack messages we are skipping so they are not redelivered
                    await msg.ack()
                    print(f"📊 [ANALYTICS] Sampled out: {msg.data.decode()}")

            if batch_to_process:
                print(
                    f"📊 [ANALYTICS] Processing batch of {len(batch_to_process)} sampled messages..."
                )
                # Simulate batch processing (e.g., aggregating, sending to DB)
                for msg in batch_to_process:
                    print(f"   -> {msg.data.decode()}")
                    await asyncio.sleep(0.1)
                # Ack the entire processed batch
                for msg in batch_to_process:
                    await msg.ack()
                print("   ✅ Batch processed and acknowledged.")

    except asyncio.TimeoutError:
        print(f"\n{consumer_name}: No messages. Shutting down.")
    finally:
        await nc.drain()


if __name__ == "__main__":
    asyncio.run(main())
