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

    def get_live_trains(self):
        runs = TrainRun.objects.filter(
            status__in=['RUNNING', 'DELAYED']
        ).select_related('train')

        data = []

        for run in runs:
            position = run.positions.first()

            if position:
              step = self._get_simulation_step(run.train.train_number)

              simulated_latitude = position.latitude + (Decimal(step) * Decimal("0.0001"))
              simulated_longitude = position.longitude + (Decimal(step) * Decimal("0.0002"))
               
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