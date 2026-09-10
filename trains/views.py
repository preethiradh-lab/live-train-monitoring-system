from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Train, TrainRun
from .serializers import TrainPositionSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status

@api_view(['GET'])
def train_live_position(request, train_number):
    train = get_object_or_404(
    Train,
    train_number=train_number
)

    run = TrainRun.objects.filter(
        train=train,
        status__in=['RUNNING', 'DELAYED']
    ).order_by('-journey_date').first()

    if not run:
     return Response(
        {
            'message': 'No active train run found.'
        },
        status=status.HTTP_404_NOT_FOUND
    )
    position = run.positions.first()

    if not position:
      return Response(
        {
            'message': 'No position data available.'
        },
        status=status.HTTP_404_NOT_FOUND
    )

    serializer = TrainPositionSerializer(position)

    return Response({
        'train_number': train.train_number,
        'train_name': train.name,
        'status': run.status,
        'live_position': serializer.data,
    })

@api_view(['GET'])
def live_trains(request):
    runs = TrainRun.objects.filter(
        status__in=['RUNNING', 'DELAYED']
    ).select_related('train')

    data = []

    for run in runs:
        position = run.positions.first()

        if position:
            data.append({
                'train_number': run.train.train_number,
                'train_name': run.train.name,
                'status': run.status,
                'latitude': position.latitude,
                'longitude': position.longitude,
                'speed': position.speed,
                'bearing': position.bearing,
                'delay_minutes': position.delay_minutes,
                'current_station': (
                    position.current_stop.station.code
                    if position.current_stop else None
                ),
                'next_station': (
                    position.next_stop.station.code
                    if position.next_stop else None
                ),
                'recorded_at': position.recorded_at,
            })

    return Response(data)

# Create your views here.
