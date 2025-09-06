# producer.py
import asyncio
import random
from nats.aio.client import Client as NATS
from .common import *


async def main():
    nc = await NATS.connect("nats://localhost:4222")
    js = nc.jetstream()

    # Ensure the stream exists
    try:
        await js.add_stream(get_stream_config())
        print(f"Stream '{STREAM_NAME}' created.")
    except Exception:
        print(f"Stream '{STREAM_NAME}' already exists.")

    order_states = [SUBJECT_NEW, SUBJECT_PAID, SUBJECT_SHIPPED, SUBJECT_CANCELLED]
    order_id = 1000

    print("Producing order events...")
    try:
        while True:
            order_id += 1
            # Pick a random order state
            subject = random.choice(order_states)
            data = f"{subject}: OrderID #{order_id}"

            # Publish persistently to JetStream
            ack = await js.publish(subject, data.encode())
            print(f"Published [/{subject}] - {data} (Seq: {ack.seq})")

            await asyncio.sleep(1)  # Produce one event per second
    except KeyboardInterrupt:
        print("\nStopping producer.")
    finally:
        await nc.drain()


if __name__ == "__main__":
    asyncio.run(main())
