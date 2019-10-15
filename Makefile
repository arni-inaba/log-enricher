test:
	poetry run pytest -vsx tests/

lint:
	poetry run flake8 log_enricher
	poetry run mypy log_enricher
