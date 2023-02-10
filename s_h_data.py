from dataclasses import replace
import datetime
import yaml
from sqlalchemy.engine.url import URL
from triage.util.db import create_engine
from triage.experiments import MultiCoreExperiment
import logging
import pandas as pd
import os
import sys
import sys

from sqlalchemy.event import listens_for
from sqlalchemy.pool import Pool

import numpy as np
import pandas as pd

user_arg = sys.argv[1]

output_path = '/data/groups/bills1/triage_output'
user_path = '/data/groups/bills1/'+ user_arg +'/mlpolicylab_fall22_bills1'


# add logging to a file (it will also go to stdout via triage logging config)
log_filename = os.path.join(output_path,'triage.log')
logger = logging.getLogger('')
hdlr = logging.FileHandler(log_filename)
hdlr.setLevel(15)   # verbose level
hdlr.setFormatter(logging.Formatter('%(name)-30s  %(asctime)s %(levelname)10s %(process)6d  %(filename)-24s  %(lineno)4d: %(message)s', '%d/%m/%Y %I:%M:%S %p'))
logger.addHandler(hdlr)


# creating database engine
dbfile = os.path.join(user_path, 'database.yaml')

with open(dbfile, 'r') as dbf:
    dbconfig = yaml.safe_load(dbf)

print(dbconfig['role'])


# assume group role to ensure shared permissions
@listens_for(Pool, "connect")
def assume_role(dbapi_con, connection_record):
    logging.debug(f"setting role {dbconfig['role']};")
    dbapi_con.cursor().execute(f"set role {dbconfig['role']};")
    # logging.debug(f"setting role postres;")
    # dbapi_con.cursor().execute(f"set role postgres;")

db_url = URL(
    'postgres',
    host=dbconfig['host'],
    username=dbconfig['user'],
    database=dbconfig['db'],
    password=dbconfig['pass'],
    port=dbconfig['port'],
)

db_engine = create_engine(db_url)


data = pd.read_csv('data/senate_house_2009_2020.csv')

data.to_sql('s_h_members',db_engine, if_exists = 'replace')