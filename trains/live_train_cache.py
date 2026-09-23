import json
from dataclasses import asdict

from .redis_client import redis_client


def save_live_train(train_number, data):
    key = f"train:{train_number}:live"

    redis_client.set(
        key,
        json.dumps(asdict(data), default=str),
        ex=30
    )
def get_live_train(train_number):
    key = f"train:{train_number}:live"

    cached_data = redis_client.get(key)

    if cached_data is None:
        return None

    return json.loads(cached_data)

def refresh_live_train_cache(data):
    save_live_train(data.train_number, data)