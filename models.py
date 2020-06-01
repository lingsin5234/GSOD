from django.db import models

# constants
DATA_TYPES = (("PRCP", "Precipitation (mm)"), ("SNOW", "Snowfall (mm)"), ("SNWD", "Snow depth (mm)"),
              ("TAVG", "Average Temperature (C)"), ("TMAX", "Maximum temperature (C)"),
              ("TMIN", "Minimum temperature (C)"), ("WSFG", "Peak Gust Wind Speed (m/s)"),
              ("WDFG", "Peak Gust Wind Direction (degrees)"))


class Station(models.Model):

    id = models.CharField(max_length=30, primary_key=True)
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    elevation = models.FloatField()
    elevation_unit = models.CharField(max_length=15)
    us_state = models.CharField(max_length=30)

    class Meta:
        app_label = 'gsod'
        constraints = [
            models.UniqueConstraint(fields=['id', 'name'], name='unique_station')
        ]

    def __str__(self):
        return str(self.id) + ' - ' + str(self.name)


class GHCND(models.Model):

    station = models.ForeignKey(Station, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField()
    datatype = models.CharField(max_length=20, choices=DATA_TYPES, null=True, blank=True)
    attributes = models.CharField(max_length=15)
    value = models.FloatField()

    class Meta:
        app_label = 'gsod'
        constraints = [
            models.UniqueConstraint(fields=['station', 'date', 'datatype'], name='unique_ghcnd')
        ]

    def __str__(self):
        return str(self.station) + ': ' + str(self.datatype) + ' - ' + str(self.date)
