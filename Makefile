all:
	@printf "Launch configuration ${name}...\n"
	@docker compose up -d

re:
	@printf "Rebuild configuration ${name}...\n"
	@docker compose down
	@docker compose up -d --build

down:
	@printf "Stopping configuration ${name}...\n"
	@docker compose down

collect:
	@printf "Collecting static files...\n"
	@docker compose exec django python /mysite/manage.py collectstatic --noinput

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

.PHONY: all re down clean collect fclean