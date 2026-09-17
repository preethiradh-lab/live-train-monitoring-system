from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass
class LiveTrainData:
    train_number: str
    train_name: str
    status: str
    latitude: Decimal
    longitude: Decimal
    speed: Decimal | None
    bearing: Decimal | None
    delay_minutes: int
    current_station: str | None
    next_station: str | None
    recorded_at: datetime