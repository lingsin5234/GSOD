from django.db import models


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
