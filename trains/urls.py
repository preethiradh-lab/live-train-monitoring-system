from django.urls import path
from .views import train_live_position, live_trains


urlpatterns = [
    path(
        'trains/<str:train_number>/live/',
        train_live_position,
        name='train-live-position'
    ),
    path(
        'trains/live/',
        live_trains,
        name='live-trains'
    ),
]