
from django.core.management.base import BaseCommand, CommandError

from trains.providers.railradar import RailRadarProvider


class Command(BaseCommand):
    help = "Fetch one train's live data from RailRadar once"

    def add_arguments(self, parser):
        parser.add_argument(
            "train_number",
            help="Train number to query, for example 66613",
        )

    def handle(self, *args, **options):
        train_number = options["train_number"]

        try:
            provider = RailRadarProvider()
            data = provider.get_train_live_position(train_number)
        except Exception as exc:
            raise CommandError(
                f"RailRadar request failed: {exc}"
            ) from exc

        if data is None:
            self.stdout.write(
                self.style.WARNING(
                    f"No usable live position found for train {train_number}."
                )
            )
            return

        self.stdout.write(f"Train: {data.train_number} - {data.train_name}")
        self.stdout.write(f"Status: {data.status}")
        self.stdout.write(f"Coordinates: {data.latitude}, {data.longitude}")
        self.stdout.write(f"Speed: {data.speed}")
        self.stdout.write(f"Delay: {data.delay_minutes} minutes")
        self.stdout.write(f"Current station: {data.current_station}")
        self.stdout.write(f"Next station: {data.next_station}")
