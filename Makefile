.PHONY: run setup db migrate makemigrations superuser install venv freeze activate test
.SILENT:

# ---------- Main tasks ----------
run: db
	python3 manage.py runserver

setup: venv install


# ---------- Database ----------
db: makemigrations migrate

migrate:
	python3 manage.py migrate

makemigrations:
	python3 manage.py makemigrations


# ---------- Other tasks ----------
superuser:
	python3 manage.py createsuperuser

test:
	python3 manage.py test


# ---------- Virtual environment ----------
install:
	pip install -r requirements.txt

freeze:
	pip freeze > requirements.txt

venv:
	python3 -m venv venv
