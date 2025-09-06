# consumer_email.py
import asyncio
from nats.aio.client import Client as NATS
from common import STREAM_NAME


async def main():
    nc = await NATS.connect("nats://localhost:4222")
    js = nc.jetstream()

    consumer_name = "email-service"
    print(f"Starting {consumer_name}...")

    # Create a DURABLE push consumer that gets ALL messages
    psub = await js.subscribe(
        subject="orders.>",  # Listen to all order subjects
        stream=STREAM_NAME,
        durable=consumer_name,  # Survive restarts
        config=ConsumerConfig(
            deliver_policy=DeliverPolicy.ALL,  # Start from the beginning of the stream
            ack_wait=30,  # Wait 30s for an ack
        ),
    )

    async def process_email(msg):
        print(f"✉️  [EMAIL] Sending notification for: {msg.data.decode()}")
        # Simulate work (e.g., calling SendGrid API)
        await asyncio.sleep(0.2)
        await msg.ack()  # Acknowledge after successful "send"
        print(f"   ✅ Email acknowledged.")

    # Assign the callback. Messages will be pushed automatically.
    psub.cb = process_email

    print(f"✅ {consumer_name} subscribed and waiting for messages...")
    # Keep the connection alive
    await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
