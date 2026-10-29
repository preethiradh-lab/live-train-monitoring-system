from celery import shared_task

from trains.providers.factory import get_live_train_provider
from trains.live_train_cache import refresh_all_live_trains_cache
from django.conf import settings

@shared_task
def refresh_live_trains():
    provider = get_live_train_provider()

    data = provider.get_live_trains()

    refresh_all_live_trains_cache(
    data,
    provider_name=settings.LIVE_TRAIN_PROVIDER,
  )
    return f"Refreshed {len(data)} live trains"

@shared_task
def refresh_railradar_train_12675():
    provider = get_live_train_provider()

    data = provider.get_train_live_position("16843")

    if data:
        refresh_all_live_trains_cache(
            [data],
            provider_name="railradar",
        )
        return "Refreshed RailRadar train 16843"

    return "No live data returned for train 16843"
