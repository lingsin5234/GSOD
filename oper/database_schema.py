# data warehouse database schema set up is done here
# setting up the sqlite database using sqlalchemy
import sqlalchemy as sa
from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, MetaData, ForeignKey, UniqueConstraint

metadata = MetaData()

# jobs
jobs_dim = Table('jobs_dim', metadata,
                 Column('Id', Integer, primary_key=True),
                 Column('job_name', String),
                 UniqueConstraint('job_name', name='jobs_u'))

# job runs
job_runs = Table('job_runs', metadata,
                 Column('Id', Integer, primary_key=True),
                 Column('job_id', ForeignKey('jobs_dim.Id')),
                 Column('job_variable', String),
                 Column('run_time', TIMESTAMP),
                 Column('end_time', TIMESTAMP),
                 Column('status', String))

# -- below may be obsolete -- #
'''
# location dim table
locations_dim = Table('locations_dim', metadata,
                      Column('Id', Integer, primary_key=True),
                      Column('location_id', String),
                      Column('name', String),
                      Column('location_type', String),

                      UniqueConstraint('location_id', 'name', name='locations_u')
                      )

# station dim table
stations_dim = Table('stations_dim', metadata,
                     Column('Id', Integer, primary_key=True),
                     Column('station_id', String, unique=True),
                     Column('name', String),
                     Column('elevation', Float),
                     Column('elevation_unit', String),
                     Column('latitude', Float),
                     Column('longitude', Float),
                     Column('location_id', ForeignKey('locations_dim.Id')),

                     UniqueConstraint('station_id', 'name', 'location_id', name='stations_u')
                     )

# location value table
locations = Table('locations', metadata,
                  Column('Id', Integer, primary_key=True),
                  Column('location_id', ForeignKey('locations_dim.Id'), unique=True),
                  Column('min_date', Date),
                  Column('max_date', Date),
                  Column('data_coverage', Float))

# station dim table
stations = Table('stations', metadata,
                 Column('Id', Integer, primary_key=True),
                 Column('station_id', ForeignKey('stations_dim.Id'), unique=True),
                 Column('min_date', Date),
                 Column('max_date', Date),
                 Column('data_coverage', Float))

'''

# setup engine and database
engine = sa.create_engine('sqlite:///gsod_dw.db', echo=True)

# safe to call multiple times as it will FIRST check for table presence
metadata.create_all(engine)


