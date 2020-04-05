from django.db import models

# constants
DATA_TYPES = (("PRCP", "Precipitation (mm)"), ("SNOW", "Snowfall (mm)"), ("SNWD", "Snow depth (mm)"),
              ("TMAX", "Maximum temperature (C)"), ("TMIN", "Minimum temperature (C)"))


class Station(models.Model):

    id = models.CharField(max_length=30, primary_key=True)
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    elevation = models.FloatField()
    elevationUnit = models.CharField(max_length=15)
    datacoverage = models.FloatField()
    mindate = models.DateField()
    maxdate = models.DateField()

    def __str__(self):
        return self.id + ' - ' + self.name


class GHCND(models.Model):

    station = models.CharField(max_length=50)
    date = models.DateField()
    datatype = models.CharField(max_length=20, choices=DATA_TYPES, null=True, blank=True)
    attributes = models.CharField(max_length=15)
    value = models.FloatField()

    def __str__(self):
        return self.station + ': ' + self.datatype + ' - ' + str(self.date)
