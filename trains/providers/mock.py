from trains.models import TrainRun
from .base import LiveTrainProvider
from .schemas import LiveTrainData
from trains.redis_client import redis_client
from decimal import Decimal
from django.utils import timezone


class MockProvider(LiveTrainProvider):

    def _get_simulation_step(self, train_number):
     key = f"train:{train_number}:simulation_step"

     return redis_client.incr(key)

    def _get_route_position(self, train, step):
     stops = list(
        train.stops
        .select_related('station')
        .order_by('sequence')
      )

     if len(stops) < 2:
        return None

     segment_index = (step - 1) // 10
     progress = Decimal((step - 1) % 10 + 1) / Decimal("10")

     if segment_index >= len(stops) - 1:
        final_station = stops[-1].station

        return (
            final_station.latitude,
            final_station.longitude,
            final_station.code,
            None,
        )

     current_stop = stops[segment_index]
     next_stop = stops[segment_index + 1]

     current_station = current_stop.station
     next_station = next_stop.station

     latitude = (
        current_station.latitude
        + (next_station.latitude - current_station.latitude) * progress
     )

     longitude = (
        current_station.longitude
        + (next_station.longitude - current_station.longitude) * progress
     )

     return (
        latitude,
        longitude,
        current_station.code,
        next_station.code,
    )

    def get_live_trains(self):
     runs = TrainRun.objects.filter(
        status__in=['RUNNING', 'DELAYED']
     ).select_related('train')

     data = []

     for run in runs:
        position = run.positions.first()

        if position:
            step = self._get_simulation_step(
                run.train.train_number
            )

            route_position = self._get_route_position(
                run.train,
                step
            )

            if route_position is None:
                continue

            (
                simulated_latitude,
                simulated_longitude,
                current_station,
                next_station,
            ) = route_position

        data.append(
            LiveTrainData(
                train_number=run.train.train_number,
                train_name=run.train.name,
                status=run.status,
                latitude=simulated_latitude,
                longitude=simulated_longitude,
                speed=position.speed,
                bearing=position.bearing,
                delay_minutes=position.delay_minutes,
                current_station=current_station,
                next_station=next_station,
                recorded_at=timezone.now(),
            )
        )
     return data

    def get_train_live_position(self, train_number):
        runs = TrainRun.objects.filter(
            train__train_number=train_number,
            status__in=['RUNNING', 'DELAYED']
        ).select_related('train')

        run = runs.order_by('-journey_date').first()

        if not run:
            return None

        position = run.positions.first()

        if not position:
            return None


        return LiveTrainData(
    train_number=run.train.train_number,
    train_name=run.train.name,
    status=run.status,
    latitude=position.latitude,
    longitude=position.longitude,
    speed=position.speed,
    bearing=position.bearing,
    delay_minutes=position.delay_minutes,
    current_station=(
        position.current_stop.station.code
        if position.current_stop
        else None
    ),
    next_station=(
        position.next_stop.station.code
        if position.next_stop
        else None
    ),
    recorded_at=position.recorded_at,
)