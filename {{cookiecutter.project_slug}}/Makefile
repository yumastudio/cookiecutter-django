CONTAINER_PREFIX={{ cookiecutter.project_slug }}
POSTGRES_HOST={{ cookiecutter.postgres_host }}
POSTGRES_USER={{ cookiecutter.postgres_user }}
POSTGRES_PASSWORD={{ cookiecutter.postgres_password }}
POSTGRES_DB={{ cookiecutter.postgres_db }}

AWS_PROFILE={{ cookiecutter.project_slug }}
AWS_CLUSTER={{ cookiecutter.project_slug }}
AWS_ECR_URL=

download_production_db:
	pg_dump --dbname=postgresql://$(POSTGRES_USER):$(POSTGRES_PASSWORD)@$(POSTGRES_HOST)/$(POSTGRES_DB) -f dump_production.sql

import_production_db:
	docker-compose -f local.yml up -d postgres
	docker exec -it $(CONTAINER_PREFIX)_postgres_1 psql -d $(POSTGRES_DB) -U $(POSTGRES_USER) -c "drop schema public cascade; create schema public;"
	cat dump_production.sql | docker exec -i psql -d $(POSTGRES_DB) -U $(POSTGRES_USER)

tag:
	git tag -a v$(version) -m "Version $(version)"

build_production:
	git checkout master
	docker-compose -f production.yml build $(container)

aws__tag:
	aws ecr get-login-password --profile $(AWS_PROFILE) --region eu-west-3 | docker login --username AWS --password-stdin $(AWS_ECR_URL)
	docker tag $(CONTAINER_PREFIX)_$(container):latest \
	$(AWS_ECR_URL)/$(AWS_CLUSTER)-$(container):latest
	sleep 2
	docker push $(AWS_ECR_URL)/$(AWS_CLUSTER)-$(container):latest

aws__stop:
	aws ecs stop-task --profile $(AWS_PROFILE) --cluster $(AWS_CLUSTER) --task $$(aws ecs list-tasks --profile $(AWS_PROFILE) --cluster $(AWS_CLUSTER) --service-name $(service) | egrep "task/" | sed -E "s/.*task\/{{ cookiecutter.project_slug }}\/(.*)\"/\1/") > /dev/null

aws__update:
	aws ecs update-service --profile $(AWS_PROFILE) --cluster $(AWS_CLUSTER) --service $(service) --force-new-deployment > /dev/null

aws__deploy:
	make aws__stop service=$(service)
	sleep 2
	make aws__update service=$(service)

aws:
	make build_production container=django
	make aws__tag container=django
	make aws__deploy service=django
	make aws__deploy service=celery
	make aws__deploy service=flower

ovh:
	make build_production
	docker-compose -f production.yml down
	docker-compose -f production.yml up
