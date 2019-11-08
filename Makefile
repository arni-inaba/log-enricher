test:
	poetry run pytest -vsx tests/

test_%:
	poetry run pytest -vs -k $@ --pdb

lint:
	poetry run flake8 log_enricher
	poetry run mypy log_enricher
