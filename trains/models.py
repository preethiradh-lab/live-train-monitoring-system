from django.db import models

class Station(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.code} - {self.name}"

class Train(models.Model):
    TRAIN_TYPES = [
        ('EXPRESS', 'Express'),
        ('SUPERFAST', 'Superfast'),
        ('PASSENGER', 'Passenger'),
        ('SPECIAL', 'Special'),
    ]

    train_number = models.CharField(
        max_length=10,
        unique=True
    )

    name = models.CharField(
        max_length=100
    )

    train_type = models.CharField(
        max_length=20,
        choices=TRAIN_TYPES
    )

    source_station = models.ForeignKey(
        Station,
        on_delete=models.PROTECT,
        related_name='source_trains',
          null=True,
          blank=True
    )

    destination_station = models.ForeignKey(
        Station,
        on_delete=models.PROTECT,
        related_name='destination_trains',
          null=True,
           blank=True
    )

    def __str__(self):
        return f"{self.train_number} - {self.name}"

class TrainStop(models.Model):
    train = models.ForeignKey(
        Train,
        on_delete=models.CASCADE,
        related_name='stops'
    )

    station = models.ForeignKey(
        Station,
        on_delete=models.PROTECT,
        related_name='train_stops'
    )

    sequence = models.PositiveIntegerField()

    scheduled_arrival = models.TimeField(
        null=True,
        blank=True
    )

    scheduled_departure = models.TimeField(
        null=True,
        blank=True
    )

    distance_from_source = models.DecimalField(
        max_digits=8,
        decimal_places=2,                   
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['sequence']
        constraints = [
            models.UniqueConstraint(
                fields=['train', 'sequence'],
                name='unique_train_stop_sequence'
            )
        ]

    def __str__(self):
        return f"{self.train} - {self.station}"

class TrainRun(models.Model):
    RUN_STATUSES = [
        ('SCHEDULED', 'Scheduled'),
        ('RUNNING', 'Running'),
        ('DELAYED', 'Delayed'),
        ('CANCELLED', 'Cancelled'),
        ('COMPLETED', 'Completed'),
    ]

    train = models.ForeignKey(
        Train,
        on_delete=models.PROTECT,
        related_name='runs'
    )

    journey_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=RUN_STATUSES,
        default='SCHEDULED'
    )

    started_at = models.DateTimeField(
        null=True,
        blank=True
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['train', 'journey_date'],
                name='unique_train_run_per_day'
            )
        ]

    def __str__(self):
        return f"{self.train} - {self.journey_date}"

class TrainPosition(models.Model):
    train_run = models.ForeignKey(
        TrainRun,
        on_delete=models.CASCADE,
        related_name='positions'
    )

    current_stop = models.ForeignKey(
        TrainStop,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='current_positions'
    )

    next_stop = models.ForeignKey(
        TrainStop,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='next_positions'
    )

    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6
    )

    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6
    )

    speed = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True
    )

    bearing = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True
    )

    delay_minutes = models.IntegerField(
        default=0
    )

    recorded_at = models.DateTimeField()

    class Meta:
        ordering = ['-recorded_at']

    def __str__(self):
        return f"{self.train_run} - {self.recorded_at}"

class Alert(models.Model):
    ALERT_TYPES = [
        ('DELAY', 'Delay'),
        ('CANCELLATION', 'Cancellation'),
        ('UNEXPECTED_STOP', 'Unexpected Stop'),
        ('SPEED', 'Speed Alert'),
        ('NO_DATA', 'No Data'),
    ]

    SEVERITIES = [
        ('INFO', 'Info'),
        ('WARNING', 'Warning'),
        ('CRITICAL', 'Critical'),
    ]

    train_run = models.ForeignKey(
        TrainRun,
        on_delete=models.CASCADE,
        related_name='alerts'
    )

    alert_type = models.CharField(
        max_length=30,
        choices=ALERT_TYPES
    )

    severity = models.CharField(
        max_length=10,
        choices=SEVERITIES,
        default='INFO'
    )

    message = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    resolved_at = models.DateTimeField(
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.train_run} - {self.alert_type}"

        
# Create your models here.
