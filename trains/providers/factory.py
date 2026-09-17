from .mock import MockProvider


def get_live_train_provider():
    return MockProvider()