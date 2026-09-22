import logging
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .providers.factory import get_live_train_provider
from .serializers import TrainPositionSerializer
from .serializers import LiveTrainDataSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status

logger = logging.getLogger(__name__)

@api_view(['GET'])
def train_live_position(request, train_number):
    try:
        provider = get_live_train_provider()

        data = provider.get_train_live_position(train_number)

        if data is None:
            return Response(
                {'message': 'No active train position found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = LiveTrainDataSerializer(data)

        return Response(serializer.data)

    except Exception as e:
     logger.error(
        "Error retrieving live position for train %s: %s",
        train_number,
        e
     )
     return Response(
        {'message': 'Unable to retrieve live train data.'},
        status=status.HTTP_503_SERVICE_UNAVAILABLE
     )
    
@api_view(['GET'])
def live_trains(request):
    try:
        provider = get_live_train_provider()

        data = provider.get_live_trains()

        serializer = LiveTrainDataSerializer(data, many=True)

        return Response(serializer.data)

    except Exception as e:
     logger.error("Error retrieving live train data: %s", e)
     return Response(
        {'message': 'Unable to retrieve live train data.'},
        status=status.HTTP_503_SERVICE_UNAVAILABLE
     )

# Create your views here.
