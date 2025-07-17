FROM python:3.10.12

WORKDIR /social_forum

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /social_forum/

EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
