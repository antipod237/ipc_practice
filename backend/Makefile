all: run

run:
	uvicorn start:app --reload --workers 2

db-migrate:
	alembic revision --autogenerate

db-upgrade:
	alembic upgrade head

db-downgrade:
	alembic downgrade -1


test:
	psql -c "drop database if exists adsystem_test" postgres
	psql -c "drop user if exists adsystem_test_user" postgres
	psql -c "create user adsystem_test_user with encrypted password 'adsystem_test_user'" postgres
	psql -c "create database adsystem_test" postgres
	TESTING=True python3 -m pytest --cov=adsystem

test-ci:
	sudo -u postgres psql -c "drop database if exists adsystem_test"
	sudo -u postgres psql -c "drop user if exists adsystem_test_user"
	sudo -u postgres psql -c "create user adsystem_test_user with encrypted password 'adsystem_test_user'"
	sudo -u postgres psql -c "create database adsystem_test"
	TESTING=True python3 -m pytest --cov=adsystem
