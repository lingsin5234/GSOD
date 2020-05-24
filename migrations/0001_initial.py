# Generated by Django 3.0.5 on 2020-05-09 14:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
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
            ],
        ),
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('elevation', models.FloatField()),
                ('elevationUnit', models.CharField(max_length=15)),
                ('datacoverage', models.FloatField()),
                ('mindate', models.DateField()),
                ('maxdate', models.DateField()),
            ],
        ),
        migrations.AddConstraint(
            model_name='station',
            constraint=models.UniqueConstraint(fields=('id', 'name'), name='unique_station'),
        ),
        migrations.AddField(
            model_name='ghcnd',
            name='station',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='gsod.Station'),
        ),
        migrations.AddConstraint(
            model_name='ghcnd',
            constraint=models.UniqueConstraint(fields=('station', 'date', 'datatype'), name='unique_ghcnd'),
        ),
    ]