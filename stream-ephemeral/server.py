# ephemeral_server_polling.py
import asyncio
from datetime import datetime, UTC

from nats.aio.client import Client as Nats
from nats.js.api import StreamConfig


async def main():
    print("🗂️  Starting Ephemeral Server (Polling Method)...")
    nc = Nats()
    await nc.connect("nats://localhost:4222")
    js = nc.jetstream()

    # Ensure the stream exists
    await js.add_stream(StreamConfig(name="COMMANDS", subjects=["commands.>"]))

    # Track the last seen ephemeral consumer name
    target_consumer_name = None
    consumer_is_active = False

    # # --- FUNCTION: Check if our target consumer exists ---
    # await check_consumer(target_consumer_name, consumer_is_active)

    # --- MAIN LOOP: Publish and Check ---
    message_count = 0
    print("📤 Starting to publish messages...")
    while True:
        message_count += 1
        message_text = f"Poll Message #{message_count} at {datetime.now(tz=UTC)}"

        # Publish a message
        ack = await js.publish("commands.ephemeral", message_text.encode())
        print(f"📤 Published: {message_text} (Seq: {ack.seq})")

        # Check the status of our consumer
        # await check_consumer()

        print("------------------------")
        consumers = await js.consumers_info("COMMANDS")
        for c in consumers:
            print(c.name)
        print("------------------------")

        # Wait before next action
        await asyncio.sleep(2)


async def check_consumer(js, target_consumer_name, consumer_is_active):
    if target_consumer_name:
        try:
            # Try to get the consumer's info from the server
            info = await js.consumer_info("COMMANDS", target_consumer_name)
            if not consumer_is_active:
                print(f"✅ CONSUMER FOUND: '{target_consumer_name}' is alive.")
                consumer_is_active = True
        except Exception as e:
            if "consumer not found" in str(e):
                if consumer_is_active:
                    print(
                        f"❌ CONSUMER LOST: Ephemeral consumer '{target_consumer_name}' has been deleted. Client is down."
                    )
                    consumer_is_active = False
            else:
                print(f"⚠️  Error checking consumer: {e}")
    else:
        # We don't know the consumer name yet, try to find it.
        try:
            consumers = await js.consumers_info("COMMANDS")
            for consumer in consumers:
                # Look for an ephemeral consumer on our subject
                if consumer.config.filter_subject == "commands.ephemeral":
                    target_consumer_name = consumer.name
                    print(f"🔍 Found target ephemeral consumer: {target_consumer_name}")
                    consumer_is_active = True
                    break
        except Exception as e:
            print(f"Could not list consumers: {e}")

    return target_consumer_name, consumer_is_active


if __name__ == "__main__":
    asyncio.run(main())
