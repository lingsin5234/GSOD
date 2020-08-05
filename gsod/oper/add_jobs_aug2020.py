# part of the August 2020 data migration
# add gsod jobs for daily/weekly and migration
from gsod.oper import database_transactions as dbt

# add the load_ghcnd jobs
result = dbt.add_gsod_job('load_ghcnd_migrate')
print('Add load_ghcnd_migrate:', result)
result = dbt.add_gsod_job('load_ghcnd')
print('Add load_ghcnd:', result)

# add the calculate_hexGrid jobs
result = dbt.add_gsod_job('calculate_hexGrid_migrate')
print('Add calculate_hexGrid_migrate:', result)
result = dbt.add_gsod_job('calculate_hexGrid')
print('Add calculate_hexGrid:', result)

# check result
query = 'SELECT * FROM jobs_dim'
result = dbt.gsod_db_reader(query)
print(result)
