FROM python:3.11-slim-buster

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

RUN python3 init_db.py

EXPOSE 5000

ENV FLASK_APP=app.python

CMD ["flask", "run", "--host", "0.0.0.0"]