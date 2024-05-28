setup-mac:
	brew install pipx
	pipx ensurepath
	sudo pipx ensurepath --global
	pipx install poetry
	poetry install

setup:
	sudo apt update
	sudo apt install pipx
	pipx ensurepath
	sudo pipx ensurepath
	pipx install poetry
	poetry install

install:
	poetry install

install-pre-commit:
	poetry run pre-commit uninstall; poetry run pre-commit install

migrate:
	poetry run python -m core.manage migrate

migrations:
	poetry run python -m core.manage makemigrations


createsuperuser:
	poetry run python -m core.manage createsuperuser

update: install migrate ;

lint:
	poetry run pre-commit run --all-files

collect:
	poetry run python -m core.manage collectstatic

wsgi:
	poetry run python -m core.manage runmodwsgi

run:
	poetry run python -m core.manage runserver


.PHONY: install update setup
