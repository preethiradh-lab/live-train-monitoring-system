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