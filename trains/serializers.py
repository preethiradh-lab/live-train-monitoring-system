from rest_framework import serializers
from .models import TrainPosition


class TrainPositionSerializer(serializers.ModelSerializer):
    current_station = serializers.CharField(
        source='current_stop.station.code',
        read_only=True
    )

    next_station = serializers.CharField(
        source='next_stop.station.code',
        read_only=True
    )
    class Meta:
        model = TrainPosition
        fields = [
            
            'latitude',
            'longitude',
            'speed',
            'bearing',
            'delay_minutes',
            'recorded_at',
            'current_station',
            'next_station',
        ]