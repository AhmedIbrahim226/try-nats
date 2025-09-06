import asyncio

from nats.aio.client import Client as NATS
from nats.js.api import StreamConfig

STREAM_NAME = "broadcast_commands"
SUBJECT = "commands.important"


async def main():
    nc = NATS()
    await nc.connect("nats://localhost:4222")
    js = nc.jetstream()

    # Ensure the stream exists
    await js.add_stream(
        StreamConfig(name=STREAM_NAME, subjects=[SUBJECT], max_msgs=1000)
    )

    # Pre-defined list of consumers we expect to be healthy
    EXPECTED_CONSUMERS = [
        "sub-server-1",
        "sub-server-2",
        "sub-server-3",
        "sub-server-4",
    ]

    while True:
        message_data = b"Important broadcast message!"

        # Publish to the persistent stream
        ack = await js.publish(SUBJECT, message_data)
        print(f"📨 Published message (Seq: {ack.seq}) to stream '{STREAM_NAME}'")

        # Wait a moment for processing
        await asyncio.sleep(2)

        # CHECK CONSUMER STATUS
        print("\n📊 Checking consumer status:")
        all_healthy = True

        for consumer_name in EXPECTED_CONSUMERS:
            try:
                # Get info for each consumer
                consumer_info = await js.consumer_info(STREAM_NAME, consumer_name)
                pending = consumer_info.num_pending
                redeliveries = consumer_info.num_redelivered

                print(
                    f"   {consumer_name}: {pending} pending, {redeliveries} redeliveries"
                )

                if (
                    pending > 5
                ):  # Heuristic: too many pending messages might indicate trouble
                    print(
                        f"   ❌ WARNING: {consumer_name} has high pending count ({pending})!"
                    )
                    all_healthy = False
                if redeliveries > 0:
                    print(
                        f"   ⚠️  NOTE: {consumer_name} has redeliveries ({redeliveries})"
                    )

            except Exception as e:
                print(
                    f"   ❌ CRITICAL: Could not find consumer '{consumer_name}'. It may be down. Error: {e}"
                )
                all_healthy = False

        if all_healthy:
            print("✅ All consumers appear healthy.")
        else:
            print("🚨 Some consumers may be failing!")

        await asyncio.sleep(5)


if __name__ == "__main__":
    asyncio.run(main())
