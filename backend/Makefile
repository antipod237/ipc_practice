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
	psql -c "drop database if exists erp_system_test" postgres
	psql -c "drop user if exists erp_system_test_user" postgres
	psql -c "create user erp_system_test_user with encrypted password 'erp_system_test_user'" postgres
	psql -c "create database erp_system_test" postgres
	TESTING=True python3 -m pytest --cov=erpsystem

test-ci:
	sudo -u postgres psql -c "drop database if exists erp_system_test"
	sudo -u postgres psql -c "drop user if exists erp_system_test_user"
	sudo -u postgres psql -c "create user erp_system_test_user with encrypted password 'erp_system_test_user'"
	sudo -u postgres psql -c "create database erp_system_test"
	TESTING=True python3 -m pytest --cov=erpsystem
