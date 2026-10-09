import requests
from django.conf import settings
from django.utils import timezone

from .base import LiveTrainProvider
from .schemas import LiveTrainData


class RailRadarProvider(LiveTrainProvider):

    BASE_URL = "https://api.railradar.in/v1"

    def _get_headers(self):
        return {
            "Authorization": f"Bearer {settings.RAILRADAR_API_KEY}"
        }
    def _normalize_status(self, status):
     status = status.lower().strip()

     status_mapping = {
        "running": "RUNNING",
        "not-started": "SCHEDULED",
        "cancelled": "CANCELLED",
        "completed": "COMPLETED",
     }
     return status_mapping.get(status, status.upper())

    def get_train_live_position(self, train_number):

        url = f"{self.BASE_URL}/trains/{train_number}/live"

        response = requests.get(
        url,
        headers=self._get_headers(),
        params={
        "includeCoordinates": "true",
        },
        timeout=15
        )

        if response.status_code == 404:
            return None

        response.raise_for_status()

        response_data = response.json()
        data = response_data["data"]

        current_location = data.get("currentLocation") or {}
        next_halt = data.get("nextHalt") or {}

        route = data.get("route") or []

        current_station_code = current_location.get("stationCode")
        next_station_code = next_halt.get("stationCode")

        coordinates = current_location.get("coordinates") or {}

        latitude = coordinates.get("lat")
        longitude = coordinates.get("lng")
        if latitude is None or longitude is None:
            return None

        return LiveTrainData(
            train_number=data["trainNumber"],
            train_name=data["trainName"],
            status=self._normalize_status(data["status"]),
            latitude=latitude,
            longitude=longitude,
            speed=current_location.get("speedKmh"),
            bearing=current_location.get("bearingDegrees"),
            delay_minutes=data.get("delayMinutes", 0),
            current_station=current_station_code,
            next_station=next_station_code,
            recorded_at=timezone.now(),
        )

    def get_live_trains(self):
        return []