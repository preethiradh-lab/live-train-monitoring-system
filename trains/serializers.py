from rest_framework import serializers
from .models import TrainPosition
from .providers.schemas import LiveTrainData


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


class LiveTrainDataSerializer(serializers.Serializer):
    train_number = serializers.CharField()
    train_name = serializers.CharField()
    status = serializers.CharField()
    latitude = serializers.DecimalField(max_digits=9, decimal_places=6)
    longitude = serializers.DecimalField(max_digits=9, decimal_places=6)
    speed = serializers.DecimalField(
        max_digits=6,
        decimal_places=2,
        allow_null=True
    )
    bearing = serializers.DecimalField(
        max_digits=6,
        decimal_places=2,
        allow_null=True
    )
    delay_minutes = serializers.IntegerField()
    current_station = serializers.CharField(allow_null=True)
    next_station = serializers.CharField(allow_null=True)
    recorded_at = serializers.DateTimeField()