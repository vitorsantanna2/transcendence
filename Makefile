DOCKER_DJANGO=docker compose exec django
DJANGO_MANAGE=/var/www/django/manage.py
STATIC_ROOT=/var/www/django/staticfiles

all: start migrations collect
	@printf "Launching configuration ${name}...\n"

re: down start migrations clean_static_collect
	@printf "Rebuilding configuration ${name}...\n"

down:
	@printf "Stopping configuration ${name}...\n"
	@docker compose down

collect:
	@printf "Collecting static files...\n"
	@docker compose exec django python3 $(DJANGO_MANAGE) collectstatic --noinput

clean_static:
	@printf "Cleaning static files...\n"
	@$(DOCKER_DJANGO) rm -rf $(STATIC_ROOT)

clean_static_collect: clean_static collect

start:
	@printf "Starting containers...\n"
	@docker compose up -d

migrations:
	@printf "Running makemigrations and migrate...\n"
	@$(DOCKER_DJANGO) python3 $(DJANGO_MANAGE) makemigrations
	@$(DOCKER_DJANGO) python3 $(DJANGO_MANAGE) migrate

clean: down
	@printf "Cleaning configuration ${name}...\n"
	@docker system prune -a

fclean:
	@printf "Total clean of all configurations docker\n"
	@docker ps -qa | xargs -r docker stop
	@docker system prune --all --force --volumes
	@docker volume ls -q | xargs -r docker volume rm
	@docker network prune --force
	@docker volume prune --force
	@rm -rf mysite/staticfiles
	@rm -rf mysite/media
	@rm -rf /var/www/django/staticfiles
	@rm -rf /var/www/django/media
	@docker compose down --volumes --remove-orphans

.PHONY: all re down start migrations collect clean_static clean_static_collect fclean