# Backend

## Initial setup

#### Virtual environment setup
```bash
python3 -m venv .venv
```

#### Database setup
(on postgres console)
```bash
create database "erp_system_dev";
create user "erp_system_dev_user" with encrypted password 'erp_system_dev_user';
grant all privileges on database "erp_system_dev" to "erp_system_dev_user";
```

## Day-to-day setup


### unix

```bash
source .venv/bin/activate  # enter environment
```

### windows

```PowerShell
.\.venv\Scripts\Activate.ps1
```

```bash
deactivate # exit environment
```

## Requirements

```bash
pip install -r requirements.txt # after you entered environment
```

## Running (linux/os x/windows with make)

[Make for windows](https://superuser.com/a/1634350)

```bash
make run
```

## Migrations (linux/os x/windows with make)

```bash
# make automatic migration
make db-migrate

# upgrade database to head
make db-upgrade

# downgrade database at one revision
make db-downgrade
```

## Lint

```bash
flake8
```

## Running (windows without make)

```PowerShell
uvicorn start:app --reload --workers 2
```

## Migrations (windows without make)

```PowerShell
# make automatic migration
alembic revision --autogenerate

# upgrade database to head
alembic upgrade head

# downgrade database at one revision
alembic downgrade -1
```
