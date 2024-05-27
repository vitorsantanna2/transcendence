setup:
	sudo apt update
	sudo apt install pipx
	pipx ensurepath
	sudo pipx ensurepath
	pipx install poetry
	poetry install

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
