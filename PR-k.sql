-- PSA: triage_runs.run_hash = experiment_models.experiment_hash

-- Find the most recent start time of this model run
select m.model_type, m.model_id, e.evaluation_start_time
from test_results.evaluations e
	left join triage_metadata.models m
		on (e.model_id=m.model_id)
	left join triage_metadata.experiment_models em
		on (em.model_hash=m.model_hash)
where em.experiment_hash = 'd79d1a38e063e48658a79319b386af5b'
order by e.evaluation_start_time desc;

-- Find the model_id of the good models
select mg.model_type, m.model_id, avg(stochastic_value) as look_at_this
from test_results.evaluations e
	left join triage_metadata.models m
		on (e.model_id=m.model_id)
	left join triage_metadata.experiment_models em
		on (em.model_hash=m.model_hash)
	left join triage_metadata.model_groups mg
		on (mg.model_group_id=m.model_group_id)
where em.experiment_hash = 'd79d1a38e063e48658a79319b386af5b'
	and metric = 'precision@'
	and parameter = '15_pct'
	and e.evaluation_start_time = '2016-12-31 00:00:00.000'
group by mg.model_type, m.model_id
order by look_at_this desc;

-- Find the best baselines
select m.model_type, m.model_id, avg(stochastic_value) as look_at_this
from test_results.evaluations e
	left join triage_metadata.models m
		on (e.model_id=m.model_id)
	left join triage_metadata.experiment_models em
		on (em.model_hash=m.model_hash)
where em.experiment_hash = 'd79d1a38e063e48658a79319b386af5b'
	and metric = 'precision@'
	and parameter = '15_pct'
	and e.evaluation_start_time = '2016-12-31 00:00:00.000'
	and m.model_type = 'triage.component.catwalk.baselines.rankers.BaselineRankMultiFeature'
group by m.model_type, m.model_id
order by look_at_this desc;

-- Looking at a single model
select * from triage_metadata.models m 
where m.model_id = 518;
-- 521: {"rules": [{"feature": "progress_dummies_entity_id_all_bill_status_9_sum", "low_value_high_score": false}]}
-- 523: {"rules": [{"feature": "votes_entity_id_all_num_votes_count", "low_value_high_score": false}]}
-- 518: {"rules": [{"feature": "progress_dummies_entity_id_all_bill_status_2_sum", "low_value_high_score": false}]}

-- Looking at this model's evaluation times
select distinct e.model_id, e.evaluation_start_time
from test_results.evaluations e 
	join triage_metadata.models m 
		on e.model_id = m.model_id 
	join triage_metadata.experiment_models em 
		on m.model_hash = em.model_hash 
where m.hyperparameters = '{"rules": [{"feature": "progress_dummies_entity_id_all_bill_status_2_sum", "low_value_high_score": false}]}'
	and em.experiment_hash = 'd79d1a38e063e48658a79319b386af5b'
order by e.evaluation_start_time desc;

-- Find the precision of the model
select cast(substring(e.parameter from '[0-9]+') as integer) as parameter, e.stochastic_value,
    cast(e.num_positive_labels as decimal(6,1))/cast(e.num_labeled_examples as decimal(6,1)) base_rate
from test_results.evaluations e
	left join triage_metadata.models m
		on (e.model_id=m.model_id)
	left join triage_metadata.experiment_models em
		on (em.model_hash=m.model_hash)
where em.experiment_hash = 'd79d1a38e063e48658a79319b386af5b'
	and metric = 'precision@'
	and e.parameter = '15_pct'
	and e.model_id = 435
order by parameter;

-- Find the recall of the model
select cast(substring(parameter from '[0-9]+') as integer) as parameter, stochastic_value, e.model_id,
    cast(num_positive_labels as decimal(6,1))/cast(num_labeled_examples as decimal(6,1)) as base_rate
from test_results.evaluations e
	left join triage_metadata.models m
		on (e.model_id=m.model_id)
	left join triage_metadata.experiment_models em
		on (em.model_hash=m.model_hash)
where em.experiment_hash = 'd79d1a38e063e48658a79319b386af5b'
	and metric = 'recall@'
	and m.model_id = 38
order by model_id desc, parameter;

-- Validation set start times
select model_id, max(evaluation_start_time) as start_time
from test_results.evaluations e 
where model_id in (521,523,518)
group by model_id;