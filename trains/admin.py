from django.contrib import admin
from .models import (
    Station,
    Train,
    TrainStop,
    TrainRun,
    TrainPosition,
    Alert,
)

admin.site.register(Station)
admin.site.register(Train)
admin.site.register(TrainStop)
admin.site.register(TrainRun)
admin.site.register(TrainPosition)
admin.site.register(Alert)

# Register your models here.
