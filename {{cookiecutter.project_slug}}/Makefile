up:
	docker-compose -f local.yml -p {{ cookiecutter.project_slug }}_api up $(containers)

run:
	docker-compose -f local.yml -p {{ cookiecutter.project_slug }}_api run --rm $(container) $(cmd)

restart:
	docker-compose -f local.yml -p {{ cookiecutter.project_slug }}_api restart $(containers)

down:
	docker-compose -f local.yml -p {{ cookiecutter.project_slug }}_api down

build:
	git checkout master
	docker-compose -f production.yml build $(container)
	aws ecr get-login-password --profile {{ cookiecutter.project_slug }} --region eu-west-3 | docker login --username AWS --password-stdin 559097556915.dkr.ecr.eu-west-3.amazonaws.com

	make tag_container container=$(container)

tag_container:
	docker tag {{ cookiecutter.project_slug }}_api_production_$(container):latest \
	559097556915.dkr.ecr.eu-west-3.amazonaws.com/{{ cookiecutter.project_slug }}-$(container):latest
	sleep 2
	docker push 559097556915.dkr.ecr.eu-west-3.amazonaws.com/{{ cookiecutter.project_slug }}-$(container):latest

deploy_container:
	make stop_container cluster=$(cluster) service=$(service)
	sleep 2
	make update_service cluster=$(cluster) service=$(service)

stop_container:
	aws ecs stop-task --profile {{ cookiecutter.project_slug }} --cluster $(cluster) --task $$(aws ecs list-tasks --profile {{ cookiecutter.project_slug }} --cluster $(cluster) --service-name $(service) | egrep "task/" | sed -E "s/.*task\/{{ cookiecutter.project_slug }}\/(.*)\"/\1/") > /dev/null

update_service:
	aws ecs update-service --profile {{ cookiecutter.project_slug }} --cluster $(cluster) --service $(service) --force-new-deployment > /dev/null

deploy_django:
	make build container=django
	make deploy_container cluster={{ cookiecutter.project_slug }} service=django
	make deploy_container cluster={{ cookiecutter.project_slug }} service=celery
	make deploy_container cluster={{ cookiecutter.project_slug }} service=flower

deploy_nlp:
	make build container=nlp
	make deploy_container cluster={{ cookiecutter.project_slug }} service=nlp

deploy:
	make deploy_django
	make deploy_nlp

static:
	docker-compose -f production.yml run --rm django ./manage.py collectstatic

download_production_db:
	pg_dump --dbname=postgresql://{{ cookiecutter.project_slug }}:R6raJbYa0uQ8sbpRTYtQ@{{ cookiecutter.project_slug }}-django.cgmv7yfftix8.eu-west-3.rds.amazonaws.com/{{ cookiecutter.project_slug }} -f dump_production.sql

import_production_db:
	docker-compose -f local.yml -p {{ cookiecutter.project_slug }}_api up -d postgres
	docker exec -it {{ cookiecutter.project_slug }}_api_postgres_1 psql -d {{ cookiecutter.project_slug }} -U {{ cookiecutter.project_slug }} -c "drop schema public cascade; create schema public;"
	cat dump_production.sql | docker exec -i {{ cookiecutter.project_slug }}_api_postgres_1 psql -d {{ cookiecutter.project_slug }} -U {{ cookiecutter.project_slug }}

tag:
	git tag -a v$(version) -m "Version $(version)"
