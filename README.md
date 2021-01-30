## SQLAlchemy - Table of Contents
* [Climate Analysis and Exploration](#climate-analysis-and-exploration)
* [Climate Application](#climate-application)


## Climate Analysis and Exploration
This challenge required a climate analysis of the hawaii.sqlite file and was completed using SQLAlchemy ORM queries, Pandas and Matplotlib. 

The queries can be found in the climate.ipynb file and it includes the following queries:

    - The last 12 months of precipitation data.
    - List of stations and temperature observations
    - The last 12 months of temperature observation data
    - The station with the highest number of temperature observations

## Climate Application
Following the initial analysis, I designed a Flask API based on the queries to create the routes.

These routes include:

    - / 
      - Home page with a list of all routes that are available.

    - /api/v1.0/precipitation
      - A query result of the precipitation data in JSON format

    - /api/v1.0/stations
      - A JSON list of stations from the dataset

    - /api/v1.0/tobs
      - A JSON list of temperature obeservations for the previous year.

    - /api/v1.0/start_date
     - When given only the start date, there will be a JSON list of the minimum temperature, the average temperature and the maximum temperature for all dates greater than and equal to the start date.

    - /api/v1.0/start_date/end_date
    - When given the start and the end date, there will be a JSON list of the minimum temperature, the average temperature and the maximum temperature for dates between the start and end date inclusive.


    
