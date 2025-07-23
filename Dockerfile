FROM python:3.10.12

WORKDIR /social_forum

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY entrypoint.sh /social_forum/entrypoint.sh
RUN chmod +x /social_forum/entrypoint.sh

COPY . /social_forum/

ENTRYPOINT ["/social_forum/entrypoint.sh"]

EXPOSE 8000
