install:
	poetry install

migrate:
	poetry run python -m core.manage migrate

migrations:
	poetry run python -m core.manage makemigrations


createsuperuser:
	poetry run python -m core.manage createsuperuser

update: install migrate ;


run:
	poetry run python -m core.manage runserver


.PHONY: install update 
