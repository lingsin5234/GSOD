# read and write to gsod_dw database
import sqlalchemy as sa


# read from database
def gsod_db_reader(query):

    engine = sa.create_engine('sqlite:///gsod_dw.db', echo=True)
    c = engine.connect()
    try:
        results = c.execute(query).fetchall()
    except Exception as e:
        print("Something went wrong with the db_reader", e)
        c.close()
        return False

    return results


# write to database
def gsod_db_writer(query):

    engine = sa.create_engine('sqlite:///gsod_dw.db', echo=True)
    c = engine.connect()
    try:
        results = c.execute(query)
    except Exception as e:
        print("Something went wrong with the db write", e)
        c.close()
        return False

    return results


# add job
def add_gsod_job(job_name):

    engine = sa.create_engine('sqlite:///gsod_dw.db', echo=True)
    c = engine.connect()

    query = 'INSERT INTO jobs_dim (job_name) VALUES(?);'

    try:
        c.execute(query, job_name)
    except Exception as e:
        print("Something went wrong with the adding a job", e)
        c.close()
        return False

    return True

