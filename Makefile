all:
	@printf "Launch configuration ${name}...\n"
	@docker compose up -d

re:
	@printf "Rebuild configuration ${name}...\n"
	@docker compose up -d --build

down:
	@printf "Stopping configuration ${name}...\n"
	@docker compose down

clean: down
	@printf "Cleaning configuration ${name}...\n"
	@docker system prune -a

collect:
	python -m core.manage collectstatic

down:
	@printf "Stopping configuration ${name}...\n"
	@docker compose down

fclean:
	@printf "Total clean of all configurations docker\n"
	@docker stop $$(docker ps -qa)
	@docker system prune --all --force --volumes
	@docker network prune --force
	@docker volume prune --force
	@rm -rf data

.PHONY: all build down re clean fclean
