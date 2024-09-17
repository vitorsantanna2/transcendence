all:
	@printf "Launch configuration ${name}...\n"
	@docker compose up -d

re:
	@printf "Rebuild configuration ${name}...\n"
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
	@docker stop $$(docker ps -qa)
	@docker system prune --all --force --volumes
	@docker network prune --force
	@docker volume prune --force
	@rm -rf data

.PHONY: all re down clean collect fclean
