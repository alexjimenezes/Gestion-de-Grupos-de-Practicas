export PGDATABASE := psi
export PGUSER := alumnodb
export PGPASSWORD := alumnodb
export PGCLIENTENCODING := LATIN9
export PGHOST := localhost
PSQL = psql

CMD = python3 manage.py
HEROKU = heroku run export SQLITE=1 &


run:
	$(CMD) runserver

reset_db: clear_db update_db create_user

clear_db:
	@echo Clear Database
	dropdb --if-exists $(PGDATABASE)
	createdb

shell:
	@echo create psql shell
	@$(PSQL)

populate:
	@echo populate database
	python3 ./manage.py populate all 19-edat.csv 19-edat_2.csv

update_db:
	$(CMD) makemigrations
	$(CMD) migrate

create_super_user:
	$(CMD) shell -c "from core.models import Student; Student.objects.create_superuser('alumnodb', 'a@a.es', 'alumnodb')"

clear_update_db:
	@echo del migrations and make migrations and migrate
	rm -rf */migrations
	python3 ./manage.py makemigrations core
	python3 ./manage.py migrate


test_datamodel:
	$(CMD) test core.tests_models

test_services:
	$(CMD) test core.tests_services

#test_heroku:
#	$(HEROKU) $(CMD) test datamodel.tests_models.GameModelTests --keepdb & wait
#	$(HEROKU) $(CMD) test datamodel.tests_models.MoveModelTests --keepdb & wait
#	$(HEROKU) $(CMD) test datamodel.tests_models.my_tests --keepdb & wait
#
#test_query:
#	python3 test_query.py
#
#test_query_heroku:
#	$(HEROKU) python3 test_query.py
#
#git:
#	git add * && git commit && git push
#
#config_heroku:
#	heroku login
#	heroku git:remote protected-bastion-43256
#
#push_heroku:
#	git push heroku master
