import logging
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .providers.factory import get_live_train_provider
from .serializers import TrainPositionSerializer
from .serializers import LiveTrainDataSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status
from .live_train_cache import (get_live_train, 
                               refresh_live_train_cache,
                               get_all_live_trains,
                               refresh_all_live_trains_cache)
from django.conf import settings

logger = logging.getLogger(__name__)

@api_view(['GET'])
def train_live_position(request, train_number):
    try:
        provider_name = settings.LIVE_TRAIN_PROVIDER
        cached_data = get_live_train(
        train_number,
        provider_name=provider_name,
        )
        if cached_data:
            return Response(cached_data)

        if settings.LIVE_TRAIN_PROVIDER == "mock":
           provider = get_live_train_provider()
           data = provider.get_train_live_position(train_number)
        else:
           return Response(
           {"message": "Live train data is not currently cached."},
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
          )

        if data is None:
            return Response(
                {'message': 'No active train position found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        refresh_live_train_cache(
                  data,
              provider_name=provider_name,
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
        provider_name = settings.LIVE_TRAIN_PROVIDER
        cached_data = get_all_live_trains()

        if cached_data:
            return Response(cached_data)
        if settings.LIVE_TRAIN_PROVIDER == "mock":
           provider = get_live_train_provider()
           data = provider.get_live_trains()
        else:
         return Response(
          {"message": "Live train data is not currently cached."},
          status=status.HTTP_503_SERVICE_UNAVAILABLE,
           )


        if not data:
            return Response(
                {'message': 'No active trains found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        refresh_all_live_trains_cache(
          data,
         provider_name=provider_name,
         )

        serializer = LiveTrainDataSerializer(data, many=True)

        return Response(serializer.data)

    except Exception as e:
        logger.error("Error retrieving live train data: %s", e)
        return Response(
            {'message': 'Unable to retrieve live train data.'},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )

# Create your views here.
