.PHONY: run setup db migrate makemigrations superuser install venv freeze activate test serve
.SILENT:

# ---------- Run ----------
serve: db
	python3 manage.py runserver

# ---------- Database ----------
db: makemigrations migrate

makemigrations:
	python3 manage.py makemigrations

migrate:
	python3 manage.py migrate

# ---------- Virtual environment ----------
venv:
	python3 -m venv venv

install:
	pip install -r requirements.txt

freeze:
	pip freeze > requirements.txt

# ---------- Docker ----------
build:
	docker build -t social-forum:dev .

run:
	docker run --rm -p 8000:8000 social-forum:dev

# ---------- Other tasks ----------
superuser:
	python3 manage.py createsuperuser

test:
	python3 manage.py test
