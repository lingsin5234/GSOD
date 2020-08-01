from rest_framework import serializers


# Weather Stations
class WeatherStations(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    elevation = serializers.FloatField()
    elevation_unit = serializers.CharField()
    us_state = serializers.CharField()
