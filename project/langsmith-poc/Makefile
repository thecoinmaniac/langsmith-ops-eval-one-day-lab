.PHONY: install test dataset experiment feedback monitor

install:
	pip install -r requirements.txt

test:
	pytest -q

dataset:
	python scripts/create_dataset.py

experiment:
	python scripts/run_experiment.py

feedback:
	python scripts/send_sample_feedback.py

monitor:
	python scripts/monitor_runs.py
