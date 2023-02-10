import yaml
from sqlalchemy.engine.url import URL
from triage.util.db import create_engine
from triage.experiments import MultiCoreExperiment
import logging
import os
from sqlalchemy.event import listens_for
from sqlalchemy.pool import Pool

import pandas as pd

dbfile = ('/data/groups/bills1/vidisha/database.yaml')

with open(dbfile, 'r') as dbf:
    dbconfig = yaml.safe_load(dbf)

print(dbconfig['role'])


db_url = URL(
              'postgres',
              host=dbconfig['host'],
              username=dbconfig['user'],
              database=dbconfig['db'],
              password=dbconfig['pass'],
              port=dbconfig['port'],
          )
db_engine = create_engine(db_url)



## PR-k curve for ML model ##

precision_ml = pd.read_sql("""


select mg.model_type,mg.model_group_id , mg.hyperparameters, e.evaluation_start_time, stochastic_value, cast(substring(parameter FROM '[0-9]+') as integer) as parameter, cast(num_positive_labels as decimal(6,1))/cast(num_labeled_examples as decimal(6,1)) base_rate
from test_results.evaluations e left join triage_metadata.models m on (e.model_id=m.model_id)
left join triage_metadata.experiment_models em on (em.model_hash=m.model_hash)
left join triage_metadata.model_groups mg on (mg.model_group_id=m.model_group_id)
where em.experiment_hash = '8f00bc4fd7f00681b116a885813b81de' and metric = 'precision@' and 
    mg.model_group_id  = 442 and evaluation_start_time = '2016-12-31 00:00:00.000' 
order by parameter

  
 """, db_engine)

print(precision_ml)

recall_ml = pd.read_sql("""


select mg.model_type,mg.model_group_id , mg.hyperparameters, e.evaluation_start_time, stochastic_value, cast(substring(parameter FROM '[0-9]+') as integer) as parameter, cast(num_positive_labels as decimal(6,1))/cast(num_labeled_examples as decimal(6,1)) base_rate
from test_results.evaluations e left join triage_metadata.models m on (e.model_id=m.model_id)
left join triage_metadata.experiment_models em on (em.model_hash=m.model_hash)
left join triage_metadata.model_groups mg on (mg.model_group_id=m.model_group_id)
where em.experiment_hash = '8f00bc4fd7f00681b116a885813b81de' and metric = 'recall@' and 
    mg.model_group_id  = 442 and evaluation_start_time = '2016-12-31 00:00:00.000' 
order by parameter

 """, db_engine)

print(recall_ml)


import numpy as np
import matplotlib.pyplot as plt
x = np.arange(1, 101, 1)
y1 = precision_ml['stochastic_value']
y2 = recall_ml['stochastic_value']
y3 = recall_ml['base_rate']

fig, ax1 = plt.subplots()

ax2 = ax1.twinx()
ax1.plot(x, y1, 'b-')
ax1.plot(x, y3)
ax2.plot(x, y2, 'r-')

ax1.set_xlabel('percent of population')
ax1.set_ylabel('Precision', color='b')
ax2.set_ylabel('Recall', color='r')
ax1.set_ylim(-0.05,1.05)
ax2.set_ylim(-0.05,1.05)
ax1.axvline(x=15, ymin=0, ymax=1, color='orange')
plt.savefig('/data/groups/bills1/vidisha/mlpolicylab_fall22_bills1/pr-K-curve_second_best_rf')
plt.show()


