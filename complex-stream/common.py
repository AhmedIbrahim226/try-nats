# common.py
from nats.js.api import StreamConfig, RetentionPolicy, StorageType

STREAM_NAME = "ORDERS"
STREAM_SUBJECTS = ["orders.>"]  # Captures orders.new, orders.paid, etc.

# Subject to publish different order events
SUBJECT_NEW = "orders.new"
SUBJECT_PAID = "orders.paid"
SUBJECT_SHIPPED = "orders.shipped"
SUBJECT_CANCELLED = "orders.cancelled"


def get_stream_config():
    return StreamConfig(
        name=STREAM_NAME,
        subjects=STREAM_SUBJECTS,
        retention=RetentionPolicy.LIMITS,
        max_msgs=10000,
        max_age=3600,  # messages live for 1 hour
        storage=StorageType.FILE,
    )
