# consumer_shipping.py
import asyncio
from nats.aio.client import Client as NATS
from common import STREAM_NAME, SUBJECT_PAID


async def main():
    nc = await NATS.connect("nats://localhost:4222")
    js = nc.jetstream()

    consumer_name = "shipping-service"
    print(f"Starting {consumer_name}...")

    # Create a DURABLE PULL consumer with a SUBJECT FILTER
    await js.add_consumer(
        STREAM_NAME,
        config=ConsumerConfig(
            durable_name=consumer_name,
            filter_subject=SUBJECT_PAID,  # <<< CRITICAL: Only get 'orders.paid'
            ack_wait=120,  # Give us more time to pack the order
        ),
    )
    # Bind to the durable consumer
    sub = await js.pull_subscribe(SUBJECT_PAID, durable=consumer_name)

    print(f"✅ {consumer_name} subscribed to '{SUBJECT_PAID}'. Pulling messages...")

    try:
        while True:
            # Fetch up to 3 messages at a time, wait 5s for them to appear
            msgs = await sub.fetch(3, timeout=5)
            for msg in msgs:
                order_info = msg.data.decode()
                print(f"📦 [SHIPPING] Preparing shipment for: {order_info}")
                # Simulate packing a box (longer work)
                await asyncio.sleep(2)
                await msg.ack()
                print(f"   ✅ Shipment ready for: {order_info}")

    except asyncio.TimeoutError:
        print(f"\n{consumer_name}: No paid orders ready for shipping. Idling...")
        # In a real service, you'd loop and fetch again instead of exiting.
    finally:
        await nc.drain()


if __name__ == "__main__":
    asyncio.run(main())
