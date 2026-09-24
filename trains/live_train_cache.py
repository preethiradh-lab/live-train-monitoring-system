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

def refresh_all_live_trains_cache(data_list):
    for data in data_list:
        refresh_live_train_cache(data)

def get_all_live_trains():
    keys = redis_client.keys("train:*:live")

    live_trains = []

    for key in keys:
        cached_data = redis_client.get(key)

        if cached_data:
            live_trains.append(json.loads(cached_data))

    return live_trains