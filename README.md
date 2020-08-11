Global Surface Temperature Summary of the Day (GSOD)
====================================================

This repository holds the Extract, Transform and Load (ETL) scripts for the GSOD data hosted by the National Centers
for Environmental Information branch of the  National Oceanic and Atmospheric Administration (NOAA).

The purpose of this project is to run a daily ETL of the GSOD data, polish its data in the database,
build prediction models and design data visualizations with the data and models.

## USA Historic Weather Data
Currently, the Maximum Temperature (in °C) is displayed as a temperature gradient by date. This is calculated using
approximately 700 weather stations' data, and added as a layer onto the map generated using MapBox. The grid itself
is generated through the JavaScript library, Turf.js.
