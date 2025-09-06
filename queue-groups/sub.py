import asyncio
import nats


async def main():
    async def close_done():
        print("CLOSED")

    # Connect to the local NATS server
    nc = await nats.connect("nats://localhost:4222", closed_cb=close_done)

    # Define a callback function to handle received messages
    async def message_handler(msg):
        subject = msg.subject
        data = msg.data.decode()
        print(f"Received a message on '{subject}': {data}")

    # Subscribe to the subject 'greetings' and assign the callback
    # The 'greetings' subject is like a channel or topic name.
    sub = await nc.subscribe(subject="greetings", queue="q1", cb=message_handler)
    print(f"Subscribed to 'greetings'. Waiting for messages...")
    await sub.unsubscribe(limit=1)

    # Keep the subscription alive. Wait for incoming messages.
    # You can use asyncio events for more complex control.
    await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
