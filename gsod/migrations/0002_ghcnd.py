# Generated by Django 3.0.4 on 2020-04-09 03:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gsod', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GHCND',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('datatype', models.CharField(blank=True, choices=[('PRCP', 'Precipitation (mm)'), ('SNOW', 'Snowfall (mm)'), ('SNWD', 'Snow depth (mm)'), ('TAVG', 'Average Temperature (C)'), ('TMAX', 'Maximum temperature (C)'), ('TMIN', 'Minimum temperature (C)'), ('WSFG', 'Peak Gust Wind Speed (m/s)'), ('WDFG', 'Peak Gust Wind Direction (degrees)')], max_length=20, null=True)),
                ('attributes', models.CharField(max_length=15)),
                ('value', models.FloatField()),
                ('station', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='gsod.Station')),
            ],
        ),
    ]
