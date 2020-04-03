from django.db import models


class Station(models.Model):

    id = models.CharField(max_length=30, primary_key=True)
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    elevation = models.FloatField()
    elevation_unit = models.CharField(max_length=15)
    data_coverage = models.FloatField()
    min_date = models.DateField()
    max_date = models.DateField()

    def __init__(self):
        return self.id + ' - ' + self.name
