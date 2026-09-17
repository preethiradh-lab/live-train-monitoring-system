from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Train, TrainRun
from .providers.factory import get_live_train_provider
from .serializers import TrainPositionSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status

@api_view(['GET'])
def train_live_position(request, train_number):
    provider = get_live_train_provider()

    data = provider.get_train_live_position(train_number)

    if data is None:
        return Response(
            {'message': 'No active train position found.'},
            status=status.HTTP_404_NOT_FOUND
        )

    return Response(data)

@api_view(['GET'])
def live_trains(request):
    provider = get_live_train_provider()

    data = provider.get_live_trains()

    return Response(data)

# Create your views here.
