setup:
	poetry install

test:
	poetry run pytest -vsx tests/

test_%:
	poetry run pytest -vs -k $@ --pdb

lint:
	poetry run flake8 log_enricher tests
	poetry run mypy log_enricher

black:
	poetry run black $(shell git diff --name-only --diff-filter d HEAD|grep \.py$)

pre_commit:
	poetry run pre-commit install
