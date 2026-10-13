
from django.conf import settings

from .mock import MockProvider
from .railradar import RailRadarProvider


def get_live_train_provider():
    provider_name = settings.LIVE_TRAIN_PROVIDER

    if provider_name == "mock":
        return MockProvider()

    if provider_name == "railradar":
        return RailRadarProvider()

    raise ValueError(
        f"Unsupported live train provider: {provider_name}"
    )
