from django.core.management.base import BaseCommand

from trains.providers.factory import get_live_train_provider
from trains.live_train_cache import refresh_all_live_trains_cache


class Command(BaseCommand):
    help = "Refresh live train data in Redis"

    def handle(self, *args, **options):
        provider = get_live_train_provider()

        data = provider.get_live_trains()

        refresh_all_live_trains_cache(data)

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully refreshed {len(data)} live trains."
            )
        )