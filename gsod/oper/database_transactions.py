# read and write to gsod_dw database
import sqlalchemy as sa
import datetime as dte


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
        print("Something went wrong with adding a job", e)
        c.close()
        return False

    return True


# log a job run
def log_gsod_job_run(job_id, job_var, status):

    engine = sa.create_engine('sqlite:///gsod_dw.db', echo=True)
    c = engine.connect()

    run_date = dte.datetime.now()
    query = 'INSERT INTO job_runs (job_id, job_variable, run_date, status) VALUES(?,?,?,?);'

    try:
        c.execute(query, job_id, job_var, run_date, status)
    except Exception as e:
        print("Something went wrong with inserting job run", e)
        c.close()
        return False

    return True
