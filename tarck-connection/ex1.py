import nats
import json

async def main():
    nc = await nats.connect("nats://localhost:4222")

    # Subscribe to all subscription creation/destruction events for all connections
    # The pattern might vary slightly based on your NATS server configuration and version.
    sub = await nc.subscribe("$SYS.ACCOUNT.*.CONNECT.*.SUB.*")

    async def sys_event_handler(msg):
        data = json.loads(msg.data.decode())
        event_type = msg.subject.split('.')[-1] # 'CREATE' or 'DESTROY'
        subject_affected = data.get('subject', 'Unknown')
        print(f"Subscription {event_type} for subject: {subject_affected}")

    # Assign the callback to the subscription
    sub.cb = sys_event_handler

    # Keep running to listen for events
    await asyncio.Future()

asyncio.run(main())