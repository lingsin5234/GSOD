Global Surface Temperature Summary of the Day (GSOD)
====================================================

This repository holds the Extract, Transform and Load (ETL) scripts for the GSOD data hosted by the National Centers
for Environmental Information branch of the  National Oceanic and Atmospheric Administration (NOAA).

The purpose of this project is to run a daily ETL of the GSOD data, polish its data in the database,
build prediction models and design data visualizations with the data and models.

## USA Historic Weather Data
Currently, the Maximum Temperature (in °C) is displayed as a temperature gradient by date. This is calculated using
approximately 700 weather stations' data, and added as a layer onto the map generated using MapBox. The grid itself
is generated through the JavaScript library, Turf.js. The temperature layer is calculated via a Python script using
the `turfpy` library, which was based off of Turf.js.

Due to the number of calculations that need to be performed, a WORM process was created so that the weather map only
needs to retrieve the temperature layer JSON file and not have to run any client-side calculations. Starting with all
the temperatures for a particular day, a Django job sends these values to Azure Blob Storage, where an Azure Batch job
will process it. This job creates a compute node that then carries out the task of running the script. After the script
finishes, the output file (e.g. the temperature layer JSON) is stored into Blob Storage, where it is then retrieved by
the Django job and staged for the weather map page to retrieve whenever it is requested.

[Weather Map](https://portfolio.sinto-ling.ca/gsod/weather-map)

More information on the Azure Batch Compute can be found on my tutorial page:
[Azure Batch Compute](https://portfolio.sinto-ling.ca/tutorials/md/azure_batch)
