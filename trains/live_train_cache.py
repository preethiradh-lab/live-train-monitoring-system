
import json
from dataclasses import asdict

from django.conf import settings

from .redis_client import redis_client


def _cache_key(train_number, provider_name=None):
    if provider_name is None:
        provider_name = settings.LIVE_TRAIN_PROVIDER

    return f"train:{provider_name}:{train_number}:live"


def save_live_train(train_number, data,provider_name=None):
    key = _cache_key(train_number, provider_name)

    redis_client.set(
        key,
        json.dumps(asdict(data), default=str),
        ex=30,
    )



def get_live_train(train_number, provider_name=None):
    key = _cache_key(train_number, provider_name)
    cached_data = redis_client.get(key)

    if cached_data is None:
        return None

    return json.loads(cached_data)



def refresh_live_train_cache(data, provider_name=None):
    save_live_train(
        data.train_number,
        data,
        provider_name=provider_name,
    )



def refresh_all_live_trains_cache(data_list, provider_name=None):
    for data in data_list:
        refresh_live_train_cache(
            data,
            provider_name=provider_name,
        )



def get_all_live_trains():
    provider_name = settings.LIVE_TRAIN_PROVIDER
    keys = redis_client.keys(f"train:{provider_name}:*:live")

    live_trains = []

    for key in keys:
        cached_data = redis_client.get(key)

        if cached_data:
            live_trains.append(json.loads(cached_data))

    return live_trains
